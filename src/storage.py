import pickle
from pathlib import Path

from .models import AddressBook


class AddressBookStorage:
    def __init__(self, path: str):
        self.path = Path(path)

    def load_or_new(self) -> AddressBook:
        if not self.path.exists():
            return AddressBook()
        try:
            with open(self.path, "rb") as f:
                book = pickle.load(f)
                if not isinstance(book, AddressBook):
                    return AddressBook()
                self._migrate_records(book)
                return book
        except Exception:
            return AddressBook()

    @staticmethod
    def _migrate_records(book: AddressBook) -> None:
        for record in book.data.values():
            if not hasattr(record, "emails"):
                record.emails = []
            if not hasattr(record, "address"):
                record.address = None
            if not hasattr(record, "note"):
                record.note = None

    def save(self, book: AddressBook) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(book, f)
