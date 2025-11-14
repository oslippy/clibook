from .constants import Command, STORAGE_PATH
from .handlers import input_error
from .models import AddressBook
from .exceptions import InvalidInputError
from .storage import AddressBookStorage


@input_error
def parse_input(user_input: str):
    command, *args = user_input.strip().split()
    command = command.upper()

    if command not in Command.available_commands():
        raise InvalidInputError(
            f"Invalid command. Use one of commands: {', '.join(Command.available_commands())}"
        )

    command = Command[command.replace("-", "_")]
    command_name = command.name.replace("_", "-")

    needs_two = {
        Command.ADD: f"Use: {command_name} <name> <phone>",
        Command.ADD_BIRTHDAY: f"Use: {command_name} <name> <birthday>",
        Command.ADD_EMAIL: f"Use: {command_name} <name> <email>",
        Command.REMOVE_EMAIL: f"Use: {command_name} <name> <email>",
    }
    needs_three = {
        Command.CHANGE: f"Use: {command_name} <name> <old_phone> <new_phone>",
        Command.EDIT_EMAIL: f"Use: {command_name} <name> <old_email> <new_email>",
    }
    needs_one = {
        Command.PHONE: f"Use: {command_name} <name>",
        Command.SHOW_BIRTHDAY: f"Use: {command_name} <name>",
        Command.SHOW_EMAIL: f"Use: {command_name} <name>",
        Command.DELETE_NOTE: f"Use: {command_name} <name>",
        Command.SEARCH: f"Use: {command_name} <query>",
        Command.SEARCH_NOTES: f"Use: {command_name} <query>",
    }

    if command in needs_two and len(args) != 2:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {needs_two[command]}"
        )
    elif command in needs_three and len(args) != 3:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {needs_three[command]}"
        )
    elif command in needs_one and len(args) < 1:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {needs_one[command]}"
        )
    elif command in (Command.ADD_NOTE, Command.EDIT_NOTE) and len(args) < 2:
        raise InvalidInputError(
            f"Your input is incorrect. Use: {command_name} <name> <note_text>"
        )
    elif command in (Command.ALL, Command.BIRTHDAYS, Command.HELP) and len(args) != 0:
        raise InvalidInputError(
            f"Your input is incorrect. Commands '{Command.ALL}', '{Command.BIRTHDAYS}', and '{Command.HELP}' don't need additional parameters."
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
