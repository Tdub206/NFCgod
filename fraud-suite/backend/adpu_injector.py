class APDUInjector:
	def __init__(self):
		self.apdu_templates = {
			"SELECT_AID": b"\x00\xA4\x04\x00\x07\xA0\x00\x00\x00\x03\x10\x10",
			"GENERATE_AC": b"\x80\xAE\x80\x00\x2D",
			"VERIFY_PIN": b"\x00\x20\x00\x80\x08\x12\x34\x56\x78\x90\x00"
		}

	def inject_apdu(self, apdu_type):
		"""Injects predefined APDUs based on transaction flow"""
		if apdu_type in self.apdu_templates:
			injected_apdu = self.apdu_templates[apdu_type]
			print(f"Injected APDU: {injected_apdu.hex()}")
			return injected_apdu
		else:
			print(f"APDU type {apdu_type} not found.")
			return None
