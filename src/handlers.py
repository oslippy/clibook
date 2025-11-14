from typing import List, Dict

from prettytable import PrettyTable

from .exceptions import AddressBookError, RecordNotFoundError, InvalidDaysError, EditCommandNotFound
from .models import AddressBook, Record, EditField


_COMMAND_DESCRIPTIONS: Dict[str, str] = {
    "hello": "Get a greeting from the bot.",
    "add": "Add a new contact or a new phone to an existing contact. A phone number must be 10 digits long and contain digits only.",
    "change": "Change a phone number for a contact. A phone number must be 10 digits long and contain digits only.",
    "phone": "Show all phone numbers for a contact.",
    "all": "Show all contacts in the address book.",
    "add-birthday": "Add a birthday for a contact.",
    "show-birthday": "Show the birthday for a contact.",
    "birthdays": "Show the upcoming birthdays within the specified number of days.",
    "help": "Show this help message.",
    "close": "Close the program.",
    "edit": (
        "Edit an existing contact field.\n"
        "Supported fields: phone, email, address, birthday.\n"
        "For phone/email you must provide old and new values.\n"
        "For address/birthday only a new value is required."
    ),
    "delete": "Delete contact in the address book."
}

_COMMAND_USAGE: Dict[str, str] = {
    "hello": "hello",
    "add": "add [name] [phone]",
    "change": "change [name] [old phone] [new phone]",
    "phone": "phone [name]",
    "all": "all",
    "add-birthday": "add-birthday [name] [DD.MM.YYYY]",
    "show-birthday": "show-birthday [name]",
    "birthdays": "birthdays [days]",
    "help": "help",
    "close": "close, exit",
    "edit": (
        "edit [name] phone [old phone] [new phone]\n"
        "edit [name] email [old email] [new email]\n"
        "edit [name] address [new address]\n"
        "edit [name] birthday [DD.MM.YYYY]"
    ),
    "delete": "delete [name]"
}

_COMMON_COUNT_DAYS = 7


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
    if record.birthday is None:
        return f"Contact '{name}' doesn't have a birthday set."
    return str(record.birthday)


def change_phone(args: List[str], address_book: AddressBook) -> str:
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
def birthdays(args: List[str], address_book: AddressBook) -> str:
    days = 0
    if len(args) == 0:
        days = _COMMON_COUNT_DAYS
    else:
        if(int(args[0]) < 0):
            raise InvalidDaysError(f"The number of days cannot be negative.")
        days = int(args[0])
    table = PrettyTable(
        title="UPCOMING BIRTHDAYS", field_names=["Name", "Congratulation Date"]
    )
    table.add_rows(
        [
            [x["name"], x["congratulation_date"]]
            for x in address_book.get_upcoming_birthdays(days)
        ]
    )
    return str(table)


def show_help(*args, **kwargs) -> str:
    table = PrettyTable(title="AVAILABLE COMMANDS", field_names=["Command", "Description"])
    table.align["Command"] = "l"
    table.align["Description"] = "l"

    for cmd in _COMMAND_DESCRIPTIONS:
        usage = "close, exit" if cmd == "close" else _COMMAND_USAGE[cmd]
        table.add_row([usage, _COMMAND_DESCRIPTIONS[cmd]])

    return str(table)

@input_error
def edit_contact(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 3:
        return "Usage: edit <name> <field> <value>"

    name = args[0]
    field_str = args[1]
    rest = args[2:]

    try:
        field = EditField.from_str(field_str)
    except ValueError as ex:
        raise EditCommandNotFound(f"Edit '{field_str}' command doesn't exist.")

    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")

    if field in (EditField.PHONE, EditField.EMAIL):
        if len(rest) != 2:
            return (
                "Usage for phone/email: "
                "edit <name> phone <old_phone> <new_phone> | "
                "edit <name> email <old_email> <new_email>"
            )

        old_value, new_value = rest

        if field == EditField.PHONE:
            record.edit_phone(old_value, new_value)
            return (
                f"Phone for '{name}' updated: '{old_value}' → '{new_value}'"
            )

        if field == EditField.EMAIL:
            pass

    if field == EditField.ADDRESS:
        pass

    if field == EditField.BIRTHDAY:
        if len(rest) != 1:
            return "Usage: edit <name> birthday <DD.MM.YYYY>"

        new_birthday_str = rest[0]
        record.edit_birthday(new_birthday_str)
        return f"Birthday for '{name}' updated to '{new_birthday_str}'"

    return "Nothing was updated"

@input_error
def delete_user(args: List[str], address_book: AddressBook):
    name = args[0]
    address_book.delete(name)
    return "Contact was deleted"