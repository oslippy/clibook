from .constants import Command, STORAGE_PATH
from .handlers import input_error, show_help
from .models import AddressBook
from .exceptions import InvalidInputError
from .storage import AddressBookStorage


@input_error
def parse_input(user_input: str):
    command, *args = user_input.strip().split()
    command = command.upper()

    if command not in Command.available_commands():
        raise InvalidInputError(f"Invalid command.\n{show_help([])}")

    command = Command[command.replace("-", "_")]
    command_name = command.name.replace("_", "-")

    exact_two = {
        Command.ADD: "<name> <phone>",
        Command.ADD_BIRTHDAY: "<name> <birthday>",
        Command.ADD_EMAIL: "<name> <email>",
        Command.REMOVE_EMAIL: "<name> <email>",
    }
    at_least_three = {
        Command.EDIT: "<name> <field> <value>",
    }
    at_least_two = {
        Command.ADD_ADDRESS: "<name> <address>",
        Command.EDIT_ADDRESS: "<name> <address>",
        Command.ADD_NOTE: "<name> <note_text>",
        Command.EDIT_NOTE: "<name> <note_text>",
    }
    at_least_one = {
        Command.PHONE: "<name>",
        Command.SHOW_BIRTHDAY: "<name>",
        Command.SHOW_EMAIL: "<name>",
        Command.SHOW_ADDRESS: "<name>",
        Command.DELETE_NOTE: "<name>",
        Command.REMOVE_ADDRESS: "<name>",
        Command.SEARCH: "<query>",
        Command.SEARCH_NOTES: "<query>",
        Command.DELETE: "<name>",
    }
    no_args = {Command.ALL, Command.BIRTHDAYS, Command.HELP}

    text_commands = {
        Command.ADD_ADDRESS,
        Command.EDIT_ADDRESS,
        Command.ADD_NOTE,
        Command.EDIT_NOTE,
    }

    if command in text_commands:
        if len(args) < 2:
            allowed = "<address>" if "ADDRESS" in command.name else "<note_text>"
            raise InvalidInputError(
                f"Your input is incorrect. Use: {command_name} <name> {allowed}"
            )
        name, *text_parts = args
        joined_text = " ".join(text_parts).strip()
        if not joined_text:
            allowed = "<address>" if "ADDRESS" in command.name else "<note_text>"
            raise InvalidInputError(
                f"Your input is incorrect. Use: {command_name} <name> {allowed}"
            )
        args = [name, joined_text]

    if command in exact_two and len(args) != 2:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command_name} {exact_two[command]}"
        )
    elif command in (Command.PHONE, Command.SHOW_BIRTHDAY) and len(args) != 1:
        use_params = (
            f"Use: {command.name} <name>"
            if command.PHONE
            else f"Use: {command.name} <name>"
        )
    elif command in at_least_three and len(args) < 3:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command_name} {at_least_three[command]}"
        )
    elif command in at_least_two and len(args) < 2:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command_name} {at_least_two[command]}"
        )
    elif command in at_least_one and len(args) < 1:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command_name} {at_least_one[command]}"
        )
    elif command in no_args and len(args) != 0:
        raise InvalidInputError(
            f"Your input is incorrect. Command '{command_name}' doesn't need additional parameters."
        )

    return command, args


def main():
    storage = AddressBookStorage(STORAGE_PATH)
    address_book: AddressBook = storage.load_or_new()
    print("Welcome to the assistant bot!")
    while True:
        input_command = input("Enter a command: ")
        if not input_command:
            print(f"Use one of commands: {', '.join(Command.available_commands())}")
            continue

        parsed_input = parse_input(input_command)
        if parsed_input is None:
            continue

        command, args = parsed_input
        if command in (Command.EXIT, Command.CLOSE):
            print("Good bye!")
            storage.save(address_book)
            break
        elif command == Command.HELLO:
            print("Hello! How can I help you?")
        else:
            result = command.func(args, address_book=address_book)
            if result is not None:
                print(result)
