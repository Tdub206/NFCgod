import serial
import sqlite3
import time

class MassCardSniffer:
	def __init__(self, db_file="captured_cards.db", port="/dev/ttyUSB0", baudrate=9600):
		self.db_file = db_file
		self.serial_conn = serial.Serial(port, baudrate, timeout=1)
		self._setup_database()
		self.sniffed_uids = set()

	def _setup_database(self):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS captured_cards (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT,
				uid TEXT UNIQUE,
				arqc TEXT,
				apdu_request TEXT,
				apdu_response TEXT
			)
		""")
		conn.commit()
		conn.close()

	def start_sniffing(self):
		"""Sniffs NFC transactions & stores unique cards"""
		print("🔥 MaxiProx ready. Scanning for NFC cards...")
		while True:
			data = self.serial_conn.readline()
			if data:
				self._process_card(data.decode().strip())

	def _process_card(self, raw_data):
		"""Processes card data, avoiding duplicates"""
		uid, apdu_request, apdu_response = self._parse_sniffed_data(raw_data)
		if uid in self.sniffed_uids:
			print(f"🚫 Skipping duplicate card: {uid}")
			return
		self.sniffed_uids.add(uid)

		fake_arqc = self._generate_fake_arqc()
		self._save_data(uid, apdu_request, apdu_response, fake_arqc)
		print(f"✅ Captured Card {uid} | ARQC: {fake_arqc.hex()}")

	def _parse_sniffed_data(self, raw_data):
		"""Extracts card UID, APDU request, and response"""
		parts = raw_data.split(",")
		return parts[0], parts[1], parts[2]

	def _generate_fake_arqc(self):
		"""Generates a placeholder ARQC (to be replaced later)"""
		return bytes.fromhex("CAFEBABEDEADBEEF")

	def _save_data(self, uid, apdu_request, apdu_response, arqc):
		"""Stores captured card data"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			INSERT OR IGNORE INTO captured_cards (timestamp, uid, apdu_request, apdu_response, arqc)
			VALUES (datetime('now'), ?, ?, ?, ?)
		""", (uid, apdu_request, apdu_response, arqc))
		conn.commit()
		conn.close()
