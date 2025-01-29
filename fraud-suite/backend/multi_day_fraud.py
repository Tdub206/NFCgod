class MultiDayFraudPlanner:
	def __init__(self, db_file="fraud_plan.json"):
		self.db_file = db_file
		self.fraud_plan = self._load_fraud_plan()

	def _load_fraud_plan(self):
		"""Load or initialize the fraud plan."""
		if not os.path.exists(self.db_file):
			return {}
		with open(self.db_file, "r") as f:
			return json.load(f)

	def _save_fraud_plan(self):
		"""Save the fraud plan to disk."""
		with open(self.db_file, "w") as f:
			json.dump(self.fraud_plan, f)

	def plan_fraud(self, cards, days=3):
		"""Generate a fraud plan over multiple days."""
		for card in cards:
			self.fraud_plan[card["uid"]] = {
				"schedule": self._generate_daily_schedule(days),
				"total_stolen": 0,
			}
		self._save_fraud_plan()

	def _generate_daily_schedule(self, days):
		"""Generate a schedule of transactions for the next few days."""
		schedule = []
		start_date = datetime.now()
		for day in range(days):
			num_transactions = random.randint(3, 8)  # Random number of transactions per day
			for _ in range(num_transactions):
				time_offset = timedelta(minutes=random.randint(0, 1440))  # Random time in the day
				schedule.append((start_date + timedelta(days=day) + time_offset).isoformat())
		return sorted(schedule)

	def execute_scheduled_fraud(self, fraud_engine):
		"""Execute transactions based on the scheduled fraud plan."""
		now = datetime.now()
		for uid, details in self.fraud_plan.items():
			schedule = details["schedule"]
			for transaction_time in schedule[:]:  # Copy the schedule to allow modification
				if datetime.fromisoformat(transaction_time) <= now:
					amount = fraud_engine._random_amount()
					fraud_engine._execute_transaction({"uid": uid, "apdu_request": self._get_apdu(uid)}, amount)
					details["total_stolen"] += amount
					schedule.remove(transaction_time)
		self._save_fraud_plan()

	def _get_apdu(self, uid):
		"""Retrieve the APDU for a given card UID."""
		# Fetch APDU from sniffed card database
		conn = sqlite3.connect("sniffed_cards.db")
		cursor = conn.cursor()
		cursor.execute("SELECT apdu_request FROM sniffed_data WHERE uid = ?", (uid,))
		result = cursor.fetchone()
		conn.close()
		return result[0] if result else None
