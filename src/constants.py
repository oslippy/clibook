"""Global constants and command registry used by the CLI."""

from enum import Enum
from typing import List

from .handlers import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    add_note,
    birthdays,
    delete_note,
    delete_user,
    edit_address,
    edit_contact,
    edit_email,
    edit_note,
    remove_address,
    remove_email,
    search_contacts,
    search_notes,
    search_tags,
    show_address,
    show_all,
    show_birthday,
    show_email,
    show_help,
    show_phone,
    sort_tags
)

STORAGE_PATH = "data/addressbook.pkl"


class Command(Enum):
    """Command registry: maps command names to ordering and handler functions."""
    ADD = 0, add_contact
    EDIT = 1, edit_contact
    CLOSE = 2, None
    EXIT = 3, None
    HELLO = 4, None
    PHONE = 5, show_phone
    ALL = 6, show_all
    ADD_BIRTHDAY = 7, add_birthday
    SHOW_BIRTHDAY = 8, show_birthday
    BIRTHDAYS = 9, birthdays
    ADD_EMAIL = 10, add_email
    REMOVE_EMAIL = 11, remove_email
    EDIT_EMAIL = 12, edit_email
    SHOW_EMAIL = 13, show_email
    ADD_ADDRESS = 14, add_address
    EDIT_ADDRESS = 15, edit_address
    REMOVE_ADDRESS = 16, remove_address
    SHOW_ADDRESS = 17, show_address
    SEARCH = 18, search_contacts
    ADD_NOTE = 19, add_note
    EDIT_NOTE = 20, edit_note
    DELETE_NOTE = 21, delete_note
    SEARCH_NOTES = 22, search_notes
    DELETE = 23, delete_user
    HELP = 24, show_help
    SEARCH_TAGS = 25, search_tags
    SORT_TAGS = 26, sort_tags

    def __init__(self, order, func):
        self.order = order
        self.func = func

    @classmethod
    def available_commands(cls) -> List[str]:
        """Return CLI-friendly command names.

        Returns:
            List[str]: All command names formatted with hyphens.
        """
        return [x.name.replace("_", "-") for x in cls]
