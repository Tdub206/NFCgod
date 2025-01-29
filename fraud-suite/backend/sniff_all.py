import nfc
import sqlite3
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet

class MaxiproxSniffer:
	def __init__(self, device="usb", db_file="sniffed_cards.db"):
		self.device = device
		self.db_file = db_file
		self.encryption_key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
		self.crypto = Fernet(self.encryption_key)
		self.aids = [
			"A0000000031010",  # Visa
			"A0000000041010",  # Mastercard
			"A000000025010402",  # Amex
		]
		self._setup_database()

	def _setup_database(self):
		"""Initialize the database for storing sniffed data."""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS sniffed_data (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT,
				uid TEXT,
				aid TEXT,
				apdu_request TEXT,
				apdu_response TEXT
			)
		""")
		conn.commit()
		conn.close()

	def _save_sniffed_data(self, uid, aid, apdu_request, apdu_response):
		"""Encrypt and save sniffed data to the database."""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		encrypted_request = self.crypto.encrypt(apdu_request.encode())
		encrypted_response = self.crypto.encrypt(apdu_response.encode())
		cursor.execute("""
			INSERT INTO sniffed_data (timestamp, uid, aid, apdu_request, apdu_response)
			VALUES (?, ?, ?, ?, ?)
		""", (datetime.now().isoformat(), uid, aid, encrypted_request, encrypted_response))
		conn.commit()
		conn.close()
		print(f"Saved card data: UID={uid}, AID={aid}")

	def sniff_all_cards(self):
		"""Continuously sniff cards and save their data."""
		print("Starting sniff-all mode...")
		with nfc.ContactlessFrontend(self.device) as clf:
			while True:
				clf.connect(rdwr={
					"on-connect": lambda tag: self._process_card(tag),
				})

	def _process_card(self, tag):
		"""Process a detected card."""
		uid = tag.identifier.hex()
		print(f"Detected card: UID {uid}")
		for aid in self.aids:
			print(f"Trying AID {aid}...")
			select_aid_apdu = bytes.fromhex(f"00A40400{len(aid) // 2:02X}{aid}")
			try:
				response = tag.exchange(select_aid_apdu)
				print(f"AID {aid} -> Response: {response.hex()}")
				self._save_sniffed_data(uid, aid, select_aid_apdu.hex(), response.hex())
			except nfc.clf.ProtocolError:
				print(f"AID {aid} failed. Retrying...")
