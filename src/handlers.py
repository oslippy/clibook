from typing import List, Dict

from prettytable import PrettyTable

from .exceptions import AddressBookError, RecordNotFoundError
from .models import AddressBook, Record


_COMMAND_DESCRIPTIONS: Dict[str, str] = {
    "hello": "Get a greeting from the bot.",
    "add": "Add a new contact or a new phone to an existing contact. A phone number must be 10 digits long and contain digits only.",
    "change": "Change a phone number for a contact. A phone number must be 10 digits long and contain digits only.",
    "phone": "Show all phone numbers for a contact.",
    "all": "Show all contacts in the address book.",
    "add-birthday": "Add a birthday for a contact.",
    "show-birthday": "Show the birthday for a contact.",
    "birthdays": "Show upcoming birthdays for the next week.",
    "add-email": "Add an email address to a contact.",
    "remove-email": "Remove an email address from a contact.",
    "edit-email": "Edit an email address for a contact.",
    "show-email": "Show all email addresses for a contact.",
    "search": "Search for contacts by a name substring.",
    "help": "Show this help message.",
    "close": "Close the program.",
}

_COMMAND_USAGE: Dict[str, str] = {
    "hello": "hello",
    "add": "add [name] [phone]",
    "change": "change [name] [old phone] [new phone]",
    "phone": "phone [name]",
    "all": "all",
    "add-birthday": "add-birthday [name] [DD.MM.YYYY]",
    "show-birthday": "show-birthday [name]",
    "birthdays": "birthdays",
    "add-email": "add-email [name] [email]",
    "remove-email": "remove-email [name] [email]",
    "edit-email": "edit-email [name] [old email] [new email]",
    "show-email": "show-email [name]",
    "search": "search [query]",
    "help": "help",
    "close": "close, exit",
}


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
def add_email(args: List[str], address_book: AddressBook) -> str:
    name, email = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    record.add_email(email)
    return "Email added."


@input_error
def remove_email(args: List[str], address_book: AddressBook) -> str:
    name, email = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    record.remove_email(email)
    return "Email removed."


@input_error
def edit_email(args: List[str], address_book: AddressBook) -> str:
    name, old_email, new_email = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    record.edit_email(old_email, new_email)
    return "Email updated."


@input_error
def show_email(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    return f"{[x.value for x in record.emails]}"


@input_error
def show_all(_: List[str], address_book: AddressBook) -> str:
    if address_book.is_empty:
        raise AddressBookError("Address Book is empty...")
    table = PrettyTable(title="CONTACTS", field_names=["Name", "Phones", "Emails", "Address", "Birthday"])
    table.add_rows(
        [
            [
                record.name,
                [x.value for x in record.phones],
                [x.value for x in record.emails] if record.emails else "N/A",
                record.address.value if record.address else "N/A",
                record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A",
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


@input_error
def search_contacts(args: List[str], address_book: AddressBook) -> str:
    """
    Search for contacts by a name substring and display results in a table.
    """
    query = args[0]
    found_records: List[Record] = address_book.search_contacts(query)

    if not found_records:
        return f"No contacts found matching '{query}'."

    # Create a table to display results
    table = PrettyTable(
        title=f"SEARCH RESULTS FOR '{query.upper()}'",
        field_names=["Name", "Phones", "Emails", "Address", "Birthday"]
    )
    table.align["Name"] = "l"
    table.align["Phones"] = "l"
    table.align["Emails"] = "l"
    table.align["Address"] = "l"
    table.align["Birthday"] = "l"

    for record in found_records:
        table.add_row(
            [
                record.name.value,
                "; ".join([phone.value for phone in record.phones]) if record.phones else "N/A",
                "; ".join([email.value for email in record.emails]) if record.emails else "N/A",
                record.address.value if record.address else "N/A",
                record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A",
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
