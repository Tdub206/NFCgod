class ISO7816Aligner:
	def __init__(self):
		self.iso7816_structure = {
			"CLA": b"\x00",  # Class byte
			"INS": b"\xA4",  # Instruction byte (SELECT FILE)
			"P1": b"\x04",   # Parameter 1
			"P2": b"\x00",   # Parameter 2
			"LC": b"\x02",   # Length
		}

	def align_apdu(self, apdu):
		"""Ensure APDU matches ISO 7816 structure"""
		aligned_apdu = self.iso7816_structure["CLA"] + self.iso7816_structure["INS"] + self.iso7816_structure["P1"] + self.iso7816_structure["P2"] + self.iso7816_structure["LC"] + apdu
		print(f"Aligned APDU: {aligned_apdu.hex()}")
		return aligned_apdu
