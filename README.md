# Assistant Bot CLI

Command-line personal address book with phones, emails, addresses, birthdays, and notes. Data is stored locally, so your contacts survive between runs.

## Features

- **Validated phones** – numbers are parsed via [`phonenumbers`](https://github.com/daviddrysdale/python-phonenumbers) and stored in E.164 format (e.g. `067-111-11-11` → `+380671111111`).
- **Rich contact records** – multiple phones, emails, a postal address, birthdays, and free-form notes.
- **Powerful editing** – dedicated commands for phones/emails plus a flexible `edit` command for phone/email/address/birthday fields.
- **Search everywhere** – lookup by name substring (`search`) or by text found inside notes (`search-notes`).
- **Tag support** – notes can include hashtags (e.g. `call #urgent`); use `search-tags` / `sort-tags` to explore them.
- **Upcoming birthdays** – `birthdays [days]` shows congratulations for the next *N* days (defaults to 7).
- **Persistent storage** – contacts are serialized to `data/addressbook.pkl` on exit and automatically reloaded.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/oslippy/clibook
   cd clibook
   ```

2. **Create a virtual environment**

   - macOS / Linux

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - Windows

     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate your virtual environment (see step 2 above).
2. Run the CLI (pick the variant that matches your OS/Python alias):

   ```bash
   python main.py
   # or
   python -m src
   ```

   On macOS/Linux you might need `python3 ...` if `python` still points to Python 2.

3. Type `help` at the prompt to see the full command list. Any unknown command automatically prints the same help output.

## Available Commands

### Core
- `hello` – friendly greeting.
- `add [name] [phone]` – create a contact or append another phone.
- `phone [name]` – show all phones for a contact.
- `all` – print the entire address book (phones, emails, address, birthday, note).
- `delete [name]` – remove a contact completely.
- `edit [name] (phone|email|address|birthday) ...` – advanced editing:
  - `edit John phone +380... +380...`
  - `edit John email old@example.com new@example.com`
  - `edit John address New Street 12`
  - `edit John birthday 10.10.1990`

### Birthdays
- `add-birthday [name] [DD.MM.YYYY]`
- `show-birthday [name]`
- `birthdays [days]` – optional `[days]` (defaults to 7).

### Email
- `add-email [name] [email]`
- `edit-email [name] [old email] [new email]`
- `remove-email [name] [email]`
- `show-email [name]`

### Address
- `add-address [name] [address ...]`
- `edit-address [name] [address ...]`
- `remove-address [name]`
- `show-address [name]`

### Notes & search
- `add-note [name] [text ...]`
- `edit-note [name] [text ...]`
- `delete-note [name]`
- `search [query]` – substring match on the contact name.
- `search-notes [query ...]` – text search inside all notes.
- `search-tags [tag]` – find contacts whose notes include the hashtag (without `#`).
- `sort-tags` – list all contacts sorted alphabetically by their first hashtag.
- `sort-tags` - sort all notes by tags alphabetically.
- `search-tags [tag]` - search notes by tag.

### System
- `help` – list every command (also shown when you type an unknown command).
- `close` / `exit` – save the book and quit the CLI.

> 💡 Tip: if you ever forget a command or type something unsupported, the CLI automatically prints the full `help` output, so you’re never stuck.