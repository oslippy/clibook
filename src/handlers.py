from typing import List

from prettytable import PrettyTable

from .exceptions import AddressBookError, RecordNotFoundError
from .models import AddressBook, Record



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, ValueError) as e:
            error_message = str(e)
            if "_contact" in error_message:
                error_message = error_message.replace("_contact", "")
            if "show_" in error_message:
                error_message = error_message.replace("show_", "")
            if "()" in error_message:
                error_message = error_message.replace("()", "")
            print(error_message)
            return None

    return inner


@input_error
def add_contact(args: List[str], address_book: AddressBook) -> str:
    name, phone_number = args
    record = address_book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        address_book.add_record(record)
        message = "Contact added."
    if phone_number:
        record.add_phone(phone_number)
    return message


@input_error
def add_birthday(args: List[str], address_book: AddressBook) -> str:
    name, birthday = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    message = "Birthday updated." if record.birthday is not None else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def show_birthday(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    return record.birthday


@input_error
def change_contact(args: List[str], address_book: AddressBook) -> str:
    name, old_number, new_number = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    record.edit_phone(old_number, new_number)
    return "Contact changed."


@input_error
def show_phone(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    return f"{[x.value for x in record.phones]}"


@input_error
def show_all(_: List[str], address_book: AddressBook) -> str:
    if address_book.is_empty:
        raise AddressBookError("Address Book is empty...")
    table = PrettyTable(title="CONTACTS", field_names=["Name", "Phones", "Birthday"])
    table.add_rows(
        [
            [
                record.name,
                [x.value for x in record.phones],
                record.birthday.value.strftime("%d.%m.%Y") if record.birthday else None,
            ]
            for _, record in address_book.records.items()
        ]
    )
    return str(table)


@input_error
def birthdays(_: List[str], address_book: AddressBook) -> str:
    table = PrettyTable(
        title="UPCOMING BIRTHDAYS", field_names=["Name", "Congratulation Date"]
    )
    table.add_rows(
        [
            [x["name"], x["congratulation_date"]]
            for x in address_book.get_upcoming_birthdays()
        ]
    )
    return str(table)