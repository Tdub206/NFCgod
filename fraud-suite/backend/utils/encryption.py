class DataRetriever:
	def __init__(self, db_file="sniffed_cards.db", encryption_key=None):
		self.db_file = db_file
		self.encryption_key = encryption_key or Fernet.generate_key()
		self.crypto = Fernet(self.encryption_key)

	def retrieve_data(self):
		"""Retrieve and decrypt all stored card data."""
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT timestamp, uid, aid, apdu_request, apdu_response FROM sniffed_data")
		results = []
		for row in cursor.fetchall():
			results.append({
				"timestamp": row[0],
				"uid": row[1],
				"aid": row[2],
				"apdu_request": self.crypto.decrypt(row[3]).decode(),
				"apdu_response": self.crypto.decrypt(row[4]).decode(),
			})
		conn.close()
		return results
