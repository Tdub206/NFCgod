class DataSyncManager:
	def __init__(self, local_db="sniffed_cards.db", server_url="https://nfc-sync-server.local"):
		self.local_db = local_db
		self.server_url = server_url

	def sync_to_server(self):
		"""Upload local data to the central server."""
		data = DataRetriever(self.local_db).retrieve_data()
		response = requests.post(f"{self.server_url}/sync", json={"data": data})
		if response.status_code == 200:
			print("Data synced successfully.")
		else:
			print(f"Sync failed: {response.status_code} - {response.text}")
