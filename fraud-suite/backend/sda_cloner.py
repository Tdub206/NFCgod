class SDACloner:
	def __init__(self, captured_static_data):
		self.static_data = captured_static_data

	def clone_card(self, target_emulator):
		"""Clone SDA data onto an NFC emulator."""
		for record in self.static_data:
			print(f"Cloning SDA record: {record['record_number']}")
			target_emulator.write_record(record["record_number"], record["data"])
		print("SDA cloning complete.")
