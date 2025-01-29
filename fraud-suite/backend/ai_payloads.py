from transformers import GPT2LMHeadModel, GPT2Tokenizer

class AIPayloadGenerator:
	def __init__(self, model_path="gpt2-arqc"):
		self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
		self.model = GPT2LMHeadModel.from_pretrained(model_path)

	def generate_apdu(self, context="EMV transaction flow"):
		"""Generate synthetic APDUs based on context."""
		input_ids = self.tokenizer.encode(context, return_tensors="pt")
		output = self.model.generate(input_ids, max_length=50, pad_token_id=self.tokenizer.eos_token_id)
		apdu_hex = self.tokenizer.decode(output[0], skip_special_tokens=True)
		return bytes.fromhex(apdu_hex)

	def generate_fake_card_data(self):
		"""Simulate fake cardholder data."""
		context = "Generate fake PAN and cryptograms for EMV card:"
		input_ids = self.tokenizer.encode(context, return_tensors="pt")
		output = self.model.generate(input_ids, max_length=100, pad_token_id=self.tokenizer.eos_token_id)
		return self.tokenizer.decode(output[0], skip_special_tokens=True)
