from Crypto.Cipher import AES
from Crypto.Hash import CMAC
import random

class ARQCForgeAI:
	def __init__(self, master_key):
		self.master_key = master_key

	def derive_session_key(self, unpredictable_number):
		"""Derives session key from the unpredictable number (UN)"""
		cmac = CMAC.new(self.master_key, ciphermod=AES)
		cmac.update(unpredictable_number + b"\x00\x00\x00\x00")
		return cmac.digest()

	def generate_arqc(self, transaction_data):
		"""Generates a forged ARQC based on transaction history"""
		session_key = self.derive_session_key(transaction_data["unpredictable_number"])
		cmac = CMAC.new(session_key, ciphermod=AES)
		cmac.update(transaction_data["raw_data"])
		forged_arqc = cmac.digest()
		print(f"Forged ARQC: {forged_arqc.hex()}")
		return forged_arqc
