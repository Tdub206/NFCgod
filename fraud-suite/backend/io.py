"""
Interfaces and mock implementations for device and database interactions.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SniffedCard:
    """Data class for sniffed card information."""
    uid: str
    aid: str
    apdu_request: str
    apdu_response: str
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class DeviceInterface(ABC):
    """Abstract interface for NFC device communication."""

    @abstractmethod
    def connect(self):
        """Connect to the device."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the device."""
        pass

    @abstractmethod
    def exchange(self, apdu: bytes) -> bytes:
        """Send APDU command and receive response."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if device is connected."""
        pass


class DatabaseInterface(ABC):
    """Abstract interface for database operations."""

    @abstractmethod
    def insert_sniffed_data(self, card: SniffedCard) -> int:
        """Insert sniffed card data. Returns the inserted record ID."""
        pass

    @abstractmethod
    def get_all_cards(self) -> List[SniffedCard]:
        """Retrieve all sniffed cards."""
        pass

    @abstractmethod
    def get_card_by_uid(self, uid: str) -> Optional[SniffedCard]:
        """Retrieve a card by UID."""
        pass

    @abstractmethod
    def delete_card(self, uid: str) -> bool:
        """Delete a card record. Returns True if successful."""
        pass

    @abstractmethod
    def close(self):
        """Close database connection."""
        pass


class MockDevice(DeviceInterface):
    """Mock implementation of DeviceInterface for testing."""

    def __init__(self):
        self._connected = False
        self.exchange_responses = {}

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    def exchange(self, apdu: bytes) -> bytes:
        """Return mock response or raise error if not configured."""
        apdu_hex = apdu.hex()
        if apdu_hex in self.exchange_responses:
            return self.exchange_responses[apdu_hex]
        # Default success response
        return bytes([0x90, 0x00])

    def is_connected(self) -> bool:
        return self._connected

    def set_response(self, apdu_hex: str, response: bytes):
        """Configure mock response for a specific APDU."""
        self.exchange_responses[apdu_hex] = response


class MockDatabase(DatabaseInterface):
    """Mock implementation of DatabaseInterface for testing."""

    def __init__(self):
        self.cards: Dict[str, SniffedCard] = {}
        self.counter = 0

    def insert_sniffed_data(self, card: SniffedCard) -> int:
        self.counter += 1
        self.cards[card.uid] = card
        return self.counter

    def get_all_cards(self) -> List[SniffedCard]:
        return list(self.cards.values())

    def get_card_by_uid(self, uid: str) -> Optional[SniffedCard]:
        return self.cards.get(uid)

    def delete_card(self, uid: str) -> bool:
        if uid in self.cards:
            del self.cards[uid]
            return True
        return False

    def close(self):
        pass
