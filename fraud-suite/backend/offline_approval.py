class OfflineApprovalEmulator:
	def __init__(self):
		self.atc = 1  # Application Transaction Counter

	def handle_apdu(self, apdu):
		"""Respond to APDUs with offline approval cryptograms."""
		if apdu[:2] == b"\x80\xAE":  # GENERATE AC
			print(f"Offline approval requested for ATC {self.atc}.")
			offline_aac = self._generate_aac(apdu)
			self.atc += 1
			return offline_aac + bytes.fromhex("90 00")  # Append success status
		return bytes.fromhex("6A 81")  # Unsupported command

	def _generate_aac(self, apdu):
		"""Generate an AAC (offline approval cryptogram)."""
		# Fake AAC (should match real cryptographic schemes for EMV)
		return bytes.fromhex("AAFFBBCCDDEEFF001122334455")
