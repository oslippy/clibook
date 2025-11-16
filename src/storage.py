"""Persistence layer for loading/saving the AddressBook using pickle."""

import pickle
from pathlib import Path

from .models import AddressBook


class AddressBookStorage:
    """File-backed storage for the AddressBook.

    Args:
        path: Filesystem path to the pickle file.
    """
    def __init__(self, path: str):
        self.path = Path(path)

    def load_or_new(self) -> AddressBook:
        """Load an AddressBook from disk or return a new empty one.

        Returns:
            AddressBook: Loaded book if the file exists and is valid, otherwise a new instance.

        Notes:
            - Any unpickling or type errors fall back to returning a new AddressBook.
            - After loading, performs migration to ensure backward compatibility of records.
        """
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
        """Ensure old pickled records have new attributes introduced over time.

        Args:
            book: AddressBook instance to migrate in-place.
        """
        for record in book.data.values():
            if not hasattr(record, "emails"):
                record.emails = []
            if not hasattr(record, "address"):
                record.address = None
            if not hasattr(record, "note"):
                record.note = None

    def save(self, book: AddressBook) -> None:
        """Persist the AddressBook to disk.

        Args:
            book: AddressBook instance to persist.

        Raises:
            OSError: If directories cannot be created or file cannot be written.
            IOError: If the file operation fails.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(book, f)
