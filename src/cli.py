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

    if command in (Command.ADD, Command.ADD_BIRTHDAY) and len(args) != 2:
        use_params = (
            f"Use: {command.name} <name> <phone>"
            if command.ADD
            else f"Use: {command.name} <name> <birthday>"
        )
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {use_params}"
        )
    elif command == Command.CHANGE and len(args) != 3:
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. Use: {command.name} "
            f"<name> <old_phone_number> <new_phone_number>"
        )
    elif command in (Command.PHONE, Command.SHOW_BIRTHDAY, Command.SEARCH) and len(args) != 1:
        use_params = ""
        if command == Command.PHONE:
            use_params = f"Use: {command.name} <name>"
        elif command == Command.SHOW_BIRTHDAY:
            use_params = f"Use: {command.name} <name>"
        elif command == Command.SEARCH:
            use_params = f"Use: {command.name} <query>"
        
        raise InvalidInputError(
            f"Your input is incorrect. You forgot additional parameters. {use_params}"
        )
    elif command in (Command.ALL, Command.BIRTHDAYS, Command.HELP) and len(args) != 0:
        raise InvalidInputError(
            f"Your input is incorrect. Commands '{Command.ALL}', '{Command.BIRTHDAYS}', and '{Command.HELP}' doesn't need additional parameters."
        )

    return command, args


def main():
    storage = AddressBookStorage(STORAGE_PATH)
    address_book: AddressBook = storage.load_or_new()
    print("Welcome to the assistant bot!")
    while True:
        input_command = input("Enter a command: ")
        if not input_command:
            print(
                f"Use one of commands: {', '.join(Command.available_commands())}"
            )
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
