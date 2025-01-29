def _log_transaction(self, card_uid, amount_cents, response):
		"""Log the transaction for auditing and analysis."""
		with open("fraud_log.json", "a") as f:
			log_entry = {
				"timestamp": datetime.now().isoformat(),
				"uid": card_uid,
				"amount_cents": amount_cents,
				"response": response.hex(),
			}
			f.write(json.dumps(log_entry) + "\n")
		print(f"Logged transaction: {log_entry}")