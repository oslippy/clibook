from typing import List, Dict

from prettytable import PrettyTable

from .exceptions import (
    AddressBookError,
    InvalidAddressError,
    InvalidSearchQueryError,
    RecordNotFoundError,
    InvalidDaysError,
    EditCommandNotFound
)
from .models import AddressBook, Record, EditField, extract_tags


_COMMAND_DESCRIPTIONS: Dict[str, str] = {
    "hello": "Get a greeting from the bot.",
    "add": "Add a new contact or a new phone to an existing contact. No spaces in phone number allowed.",
    "phone": "Show all phone numbers for a contact.",
    "all": "Show all contacts in the address book.",
    "add-birthday": "Add a birthday for a contact.",
    "show-birthday": "Show the birthday for a contact.",
    "add-email": "Add an email address to a contact.",
    "remove-email": "Remove an email address from a contact.",
    "edit-email": "Edit an email address for a contact.",
    "show-email": "Show all email addresses for a contact.",
    "search": "Search for contacts by a name substring.",
    "add-address": "Add an address to a contact.",
    "edit-address": "Edit an address for a contact.",
    "remove-address": "Remove the address from a contact.",
    "show-address": "Show the address for a contact.",
    "add-note": "Add a note to contact.",
    "edit-note": "Edit note of a contact.",
    "delete-note": "Delete note of a contact.",
    "search-notes": "Search contacts by notes.",
    "birthdays": "Show the upcoming birthdays within the specified number of days.",
    "search-tags": "Search contacts by tags in notes.",
    "sort-tags": "Sort contacts by the tags in their notes.",
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
    "phone": "phone [name]",
    "all": "all",
    "add-birthday": "add-birthday [name] [DD.MM.YYYY]",
    "show-birthday": "show-birthday [name]",
    "birthdays": "birthdays [days]",
    "add-email": "add-email [name] [email]",
    "remove-email": "remove-email [name] [email]",
    "edit-email": "edit-email [name] [old email] [new email]",
    "show-email": "show-email [name]",
    "search": "search [query]",
    "add-address": "add-address [name] [address]",
    "edit-address": "edit-address [name] [address]",
    "remove-address": "remove-address [name]",
    "show-address": "show-address [name]",
    "add-note": "add-note [name] [text]",
    "edit-note": "edit-note [name] [text]",
    "delete-note": "delete-note [name]",
    "search-notes": "search-notes <query>",
    "search-tags": "search-tags <tag>",
    "sort-tags": "sort-tags",
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


def _build_contacts_table(
    title: str, include_note: bool = False, include_tags: bool = False
) -> PrettyTable:
    field_names = ["Name", "Phones", "Emails", "Address", "Birthday"]
    if include_note:
        field_names.append("Note")
    if include_tags:
        field_names.append("Tags")
    table = PrettyTable(title=title, field_names=field_names)
    for field in field_names:
        table.align[field] = "l"
    return table


def _format_contact_row(record: Record, include_note: bool = False) -> List[str]:
    row = [
        record.name.value,
        "\n".join(phone.value for phone in record.phones) if record.phones else "N/A",
        "\n".join(email.value for email in record.emails) if record.emails else "N/A",
        record.address.value if record.address else "N/A",
        record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "N/A",
    ]
    if include_note:
        row.append(record.note or "N/A")
    return row


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
def add_address(args: List[str], address_book: AddressBook) -> str:
    name, address_text = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    if not address_text.strip():
        raise InvalidAddressError("Address cannot be empty.")
    message = "Address updated." if record.address else "Address added."
    record.set_address(address_text)
    return message


@input_error
def edit_address(args: List[str], address_book: AddressBook) -> str:
    name, address_text = args
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    if not address_text.strip():
        raise InvalidAddressError("Address cannot be empty.")
    message = "Address updated." if record.address else "Address added."
    record.set_address(address_text)
    return message


@input_error
def remove_address(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    if record.address is None:
        raise InvalidAddressError(f"Contact '{name}' does not have an address.")
    record.remove_address()
    return "Address removed."


@input_error
def show_address(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if record is None:
        raise RecordNotFoundError(f"Contact '{name}' doesn't exist.")
    if record.address is None:
        return f"Contact '{name}' doesn't have an address."
    return record.address.value


@input_error
def show_all(_: List[str], address_book: AddressBook) -> str:
    if address_book.is_empty:
        raise AddressBookError("Address Book is empty...")
    table = _build_contacts_table("CONTACTS", include_note=True)
    table.add_rows(
        [
            _format_contact_row(record, include_note=True)
            for record in address_book.records.values()
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


@input_error
def search_contacts(args: List[str], address_book: AddressBook) -> str:
    """
    Search for contacts by a name substring and display results in a table.
    """

    if not args:
        raise InvalidSearchQueryError("Please provide a search query.")

    query = args[0]
    found_records: List[Record] = address_book.search_contacts(query)

    if not found_records:
        return f"No contacts found matching '{query}'."

    table = _build_contacts_table(
        title=f"SEARCH RESULTS FOR '{query.upper()}'", include_note=True
    )

    for record in found_records:
        table.add_row(_format_contact_row(record, include_note=True))

    return str(table)


def show_help(*args, **kwargs) -> str:
    table = PrettyTable(
        title="AVAILABLE COMMANDS", field_names=["Command", "Description"]
    )
    table.align["Command"] = "l"
    table.align["Description"] = "l"

    for cmd in _COMMAND_DESCRIPTIONS:
        usage = "close, exit" if cmd == "close" else _COMMAND_USAGE[cmd]
        table.add_row([usage, _COMMAND_DESCRIPTIONS[cmd]])

    return str(table)

@input_error
def edit_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Handle the 'edit' command and update a specific field of a contact.

    Supported fields and formats:
      - phone:    edit <name> phone <old_phone> <new_phone>
      - email:    edit <name> email <old_email> <new_email>
      - address:  edit <name> address <new address>
      - birthday: edit <name> birthday <DD.MM.YYYY>

    Returns a user-friendly message or usage hint, or raises an error
    if the contact or field cannot be processed.
    """

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
            record.edit_email(old_value, new_value)
            return (
                f"Email for '{name}' updated: '{old_value}' → '{new_value}'"
            )

    if field == EditField.ADDRESS:
        if not rest:
            return "Usage: edit <name> address <new address>"
        new_address = " ".join(rest).strip()
        if not new_address:
            raise InvalidAddressError("Address cannot be empty.")
        record.set_address(new_address)
        return f"Address for '{name}' updated."

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


@input_error
def add_note(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    note_text = " ".join(args[1:])

    record = address_book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    record.set_note(note_text)
    return f"Note added to {name}."


@input_error
def edit_note(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    new_text = " ".join(args[1:])

    record = address_book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    if record.note is None:
        return f"{name} has no note to edit."

    record.set_note(new_text)
    return f"Note updated for {name}."


@input_error
def delete_note(args: List[str], address_book: AddressBook) -> str:
    name = args[0]
    record = address_book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    if record.note is None:
        return f"{name} has no note to delete."

    record.remove_note()
    return f"Note removed from {name}."


@input_error
def search_notes(args: List[str], address_book: AddressBook) -> str:
    if len(args) < 1:
        return "Usage: search-notes <query>"

    query = " ".join(args)
    results = address_book.search_by_notes(query)

    if not results:
        return "No notes found."

    table = _build_contacts_table("SEARCH NOTES RESULTS", include_note=True)

    for record in results:
        table.add_row(_format_contact_row(record, include_note=True))

    return str(table)

@input_error
def search_tags(args: List[str], address_book: AddressBook) -> str:
    query = args[0]
    results = address_book.search_by_tags(query)

    if not results:
        return f"No notes found with tag '{query}'."

    table = _build_contacts_table(
        title=f"SEARCH TAGS RESULTS FOR '{query.upper()}'", include_note=True
    )

    for record in results:
        table.add_row(_format_contact_row(record, include_note=True))

    return str(table)


@input_error
def sort_tags(args: List[str], address_book: AddressBook) -> str:
    sorted_records = address_book.sort_by_tags_alphabetically()

    if not sorted_records:
        return "Address Book is empty..."

    table = _build_contacts_table(
        title="SORTED NOTES BY TAG ALPHABETICALLY", include_note=True, include_tags=True
    )

    for record in sorted_records:
        row = _format_contact_row(record, include_note=True)
        row.append(", ".join(extract_tags(record.note)) if record.note else "N/A")
        table.add_row(row)

    return str(table)