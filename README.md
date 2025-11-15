# Assistant Bot CLI

A simple, command-line application to manage your contacts, including phones, emails, birthdays, and notes. The bot saves your data locally, so your contact book is persistent.

## Features

* **Contact Management:** Add, edit, and find contacts.
* **Detailed Records:** Store multiple phones, emails, and an address for each contact.
* **Birthday Tracking:** Add birthdays and get a list of upcoming birthdays for a specified number of days.
* **Notes:** Add, edit, or remove notes associated with a contact.
* **Robust Validation:** Uses the `phonenumbers` library to validate and standardize phone numbers (e.g., `067-111-11-11` is stored as `+380671111111`).
* **Powerful Search:**
    * Find contacts by a partial match of their name.
    * Find contacts by the content of their notes.
* **Persistent Storage:** Your address book is automatically saved on exit and reloaded on start.

## Installation

To get the application running on your local machine, follow these steps.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/oslippy/clibook
    cd clibook
    ```

2.  **Create a Virtual Environment:**
    * **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    Make sure you are in the project's root directory (where `requirements.txt` is located).
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once installed, you can run the bot from your terminal.

1.  Make sure your virtual environment is activated (see step 2 above).
2.  Run the main application module:

2.  Run the main application module:

    ```bash
    python -m src.cli
    ```
    
    Or, if `python` on your system points to an older version (like Python 2), use `python3`:
    
    ```bash
    python3 -m src.cli
    ```

    **When to use which:**
    * Use `python -m src.cli` on **Windows**, or on any system where you are sure the `python` command runs Python 3.
    * Use `python3 -m src.cli` on **macOS and Linux**, as `python` often defaults to an older Python 2 installation on those systems.

3.  You will be greeted with a welcome message and an input prompt. Type `help` to see a full list of commands.

## Available Commands

Here is a list of commands you can use:

* `hello`
    * **Description:** Get a greeting from the bot.
* `add [name] [phone]`
    * **Description:** Add a new contact or a new phone to an existing contact.
* `change [name] [old phone] [new phone]`
    * **Description:** Change a phone number for a contact. The `[old phone]` can be in any valid format (e.g., `067-111-11-11` or `+380671111111`).
* `phone [name]`
    * **Description:** Show all phone numbers for a contact.
* `all`
    * **Description:** Show all contacts in the address book.
* `add-birthday [name] [DD.MM.YYYY]`
    * **Description:** Add a birthday for a contact.
* `show-birthday [name]`
    * **Description:** Show the birthday for a contact.
* `birthdays [days]`
    * **Description:** Show upcoming birthdays for the next `[days]` days (e.g., `birthdays 10`).
* `search [query]`
    * **Description:** Search for contacts by a partial match of their name.
* `help`
    * **Description:** Show this help message.
* `close` or `exit`
    * **Description:** Save all data and close the program.

*(Note: Additional commands for email, address, and notes may also be available. Type `help` in the bot for a complete list.)*