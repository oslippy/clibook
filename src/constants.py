from enum import Enum
from typing import List

from .handlers import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    add_note,
    birthdays,
    change_contact,
    delete_note,
    edit_address,
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
    ADD = 0, add_contact
    CHANGE = 1, change_contact
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
    HELP = 19, show_help
    ADD_NOTE = 20, add_note
    EDIT_NOTE = 21, edit_note
    DELETE_NOTE = 22, delete_note
    SEARCH_NOTES = 23, search_notes
    SEARCH_TAGS = 24, search_tags
    SORT_TAGS = 25, sort_tags

    def __init__(self, order, func):
        self.order = order
        self.func = func

    @classmethod
    def available_commands(cls) -> List[str]:
        return [x.name.replace("_", "-") for x in cls]
