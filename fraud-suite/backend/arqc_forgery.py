from Crypto.Hash import CMAC
from Crypto.Cipher import AES

class ARQCForger:
	def __init__(self, master_key):
		self.master_key = master_key

	def derive_session_key(self, unpredictable_number):
		cmac = CMAC.new(self.master_key, ciphermod=AES)
		cmac.update(unpredictable_number + b"\x00\x00\x00\x00")
		return cmac.digest()

	def forge_arqc(self, transaction_data):
		session_key = self.derive_session_key(transaction_data["unpredictable_number"])
		cmac = CMAC.new(session_key, ciphermod=AES)
		cmac.update(transaction_data["raw_data"])
		return cmac.digest()