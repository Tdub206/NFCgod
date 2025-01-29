import sqlite3

class DatabaseManager:
	def __init__(self, db_file="sniffed_cards.db"):
		self.db_file = db_file
		self._setup_database()

	def _setup_database(self):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS sniffed_data (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT,
				uid TEXT,
				apdu_request TEXT,
				apdu_response TEXT
			)
		""")
		conn.commit()
		conn.close()

	def insert_sniffed_data(self, uid, apdu_request, apdu_response):
		conn = sqlite3.connect(self.db_file)
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO sniffed_data (timestamp, uid, apdu_request, apdu_response)
			VALUES (datetime('now'), ?, ?, ?)
		""", (uid, apdu_request, apdu_response))
		conn.commit()
		conn.close()
