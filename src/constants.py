from enum import Enum
from typing import List

from .handlers import (
    add_birthday,
    add_contact,
    add_email,
    birthdays,
    change_contact,
    edit_email,
    remove_email,
    show_birthday,
    show_all,
    show_email,
    show_phone,
    show_help,
    search_contacts,
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
    SEARCH = 14, search_contacts
    HELP = 15, show_help

    def __init__(self, order, func):
        self.order = order
        self.func = func

    @classmethod
    def available_commands(cls) -> List[str]:
        return [x.name.replace("_", "-") for x in cls]