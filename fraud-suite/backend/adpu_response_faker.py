class APDUResponseModifier:
	def __init__(self):
		self.success_codes = [b"\x90\x00"]  # Standard success response
		self.fallback_codes = {
			b"\x6A\x81": b"\x90\x00",  # Invalid data → Success
			b"\x6A\x88": b"\x90\x00",  # ARQC failure → Success
		}

	def modify_response(self, response):
		"""Modify APDU response if it's an error"""
		if response in self.fallback_codes:
			print(f"Modifying response {response.hex()} → {self.fallback_codes[response].hex()}")
			return self.fallback_codes[response]
		return response  # Return original if already successful
