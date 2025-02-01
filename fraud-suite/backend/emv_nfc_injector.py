import random

class EMVNFCInjector:
	def __init__(self):
		self.valid_tags = [
			b"\x5F\x20\x08JohnDoe",  # Cardholder Name
			b"\x5A\x08\x47\x61\x21\x43\x89\x01\x02\x34",  # PAN (Primary Account Number)
			b"\x9F\x10\x07\x06\x00\x00\x00\x00\x00\x00",  # Issuer Application Data
		]

	def inject_valid_tags(self, apdu):
		"""Append valid NFC tags to APDU"""
		injected_apdu = apdu + random.choice(self.valid_tags)
		print(f"Injected NFC tag: {injected_apdu.hex()}")
		return injected_apdu
