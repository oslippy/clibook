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
                return book if isinstance(book, AddressBook) else AddressBook()
        except Exception:
            return AddressBook()

    def save(self, book: AddressBook) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(book, f)
