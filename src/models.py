import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import Any, Dict, List
import phonenumbers
from enum import Enum

from .exceptions import (
    EmailNotFoundError,
    InvalidAddressError,
    InvalidBirthdayError,
    InvalidEmailError,
    InvalidNameError,
    InvalidPhoneError,
    PhoneNotFoundError,
    RecordNotFoundError,
)


class EditField(str, Enum):
    PHONE = "phone"
    EMAIL = "email"
    ADDRESS = "address"
    BIRTHDAY = "birthday"

    @classmethod
    def from_str(cls, value: str) -> "EditField":
        value = value.lower()
        try:
            return cls(value)
        except ValueError:
            raise ValueError(
                f"Unknown field '{value}'. Allowed: phone, email, address, birthday"
            )

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value or not value.strip():
            raise InvalidNameError("Name cannot be empty.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value):
        try:
            formatted_value = self._validate_phone(value)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise InvalidPhoneError(f"Could not parse phone number: '{value}'.") from e
        
        super().__init__(formatted_value)

    @staticmethod
    def _validate_phone(phone_number: str) -> str:
        """
        Validates the phone number using the phonenumbers library.
        - If a number starts with '+', it's treated as international.
        - If not, a default region is assumed (e.g., "UA" for Ukraine).
        Raises:
            InvalidPhoneError: If the number is not valid.
        Returns:
            str: The phone number in E.164 format (e.g., "+380951234567").
        """
        # Set a default region for parsing numbers without a country code.
        default_region = "UA"

        parsed_number = phonenumbers.parse(phone_number, default_region)

        if not phonenumbers.is_valid_number(parsed_number):
            raise InvalidPhoneError(f"The number '{phone_number}' is not a valid phone number.")

        # Format and return the number in E.164 standard
        formatted_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
        return formatted_number


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value.strip(), "%d.%m.%Y")
        except ValueError:
            raise InvalidBirthdayError("Invalid date format. Use DD.MM.YYYY")

        today = datetime.now().date()
        birthday_date = parsed_date.date()

        if birthday_date > today:
            raise InvalidBirthdayError("Birthday cannot be in the future.")

        super().__init__(parsed_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Email(Field):
    def __init__(self, value):
        if not self._validate_email(value):
            raise InvalidEmailError(
                "You have entered an invalid email. Please use a valid email format (e.g., user@domain.com)."
            )
        super().__init__(value.strip().lower())

    @staticmethod
    def _validate_email(email: str) -> bool:
        if not email or not email.strip():
            return False
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return bool(pattern.match(email.strip()))


class Address(Field):
    def __init__(self, value):
        if not value or not value.strip():
            raise InvalidAddressError("Address cannot be empty.")
        super().__init__(value.strip())


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.birthday = None
        self.note = None

    def __setstate__(self, state):
        self.__dict__ = state
        if not hasattr(self, "emails"):
            self.emails = []
        if not hasattr(self, "address"):
            self.address = None
        if not hasattr(self, "note"):
            self.note = None

    def add_phone(self, phone: str) -> None:
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str) -> None:
        phone_to_remove = self.find_phone(phone)
        self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_to_edit = self.find_phone(old_phone)
        idx = self.phones.index(phone_to_edit)
        self.phones[idx] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone:
        """
        Finds a phone object by its string value.
        The input 'phone' string is first normalized to E.164 format
        before comparison.
        """
        try:
            normalized_phone = Phone._validate_phone(phone)
        except (InvalidPhoneError, phonenumbers.phonenumberutil.NumberParseException):
            raise PhoneNotFoundError(f"Phone '{phone}' is not a valid phone format and was not found.") from None

        for phone_obj in self.phones:
            if phone_obj.value == normalized_phone:
                return phone_obj

        raise PhoneNotFoundError(f"Phone '{phone}' (normalized to '{normalized_phone}') not found in record {self.name.value}.")


    def find_email(self, email: str) -> Email:
        for email_obj in self.emails:
            if email_obj.value == email.lower().strip():
                return email_obj
        raise EmailNotFoundError(f"Email {email} not found in record {self.name.value}.")

    def add_email(self, email: str) -> None:
        email_obj = Email(email)
        self.emails.append(email_obj)

    def remove_email(self, email: str) -> None:
        email_to_remove = self.find_email(email)
        self.emails.remove(email_to_remove)

    def edit_email(self, old_email: str, new_email: str) -> None:
        email_to_edit = self.find_email(old_email)
        idx = self.emails.index(email_to_edit)
        self.emails[idx] = Email(new_email)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def edit_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def remove_address(self) -> None:
        self.address = None

    def __str__(self):
        parts = [f"Contact name: {self.name.value}"]
        if self.phones:
            parts.append(f"phones: {'; '.join(p.value for p in self.phones)}")
        if self.emails:
            parts.append(f"emails: {'; '.join(e.value for e in self.emails)}")
        if self.address:
            parts.append(f"address: {self.address.value}")
        return ", ".join(parts)

    def set_note(self, note: str):
        self.note = note

    def get_note(self) -> str | None:
        return self.note

    def remove_note(self):
        self.note = None


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            raise RecordNotFoundError(f"Record with name '{name}' not found.")

    def search_contacts(self, query: str) -> List[Record]:
        """
        Search for contacts by a name substring (case-insensitive).
        """
        results: List[Record] = []
        lower_query = query.lower()

        for record in self.data.values():
            if lower_query in record.name.value.lower():
                results.append(record)

        return results

    @property
    def is_empty(self) -> bool:
        return not bool(self.data)

    @property
    def records(self) -> Dict[str, Any]:
        return self.data

    def search_by_notes(self, query: str) -> List[Record]:
        lower_query = query.lower()
        results: List[Record] = []

        for record in self.data.values():
            if record.note and lower_query in record.note.lower():
                results.append(record)

        return results

    def get_upcoming_birthdays(self, days: int = 7) -> List[Dict[str, str]]:
        today_date = datetime.now().date()
        congratulation_users = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.value

            birthday_this_year = datetime(
                year=today_date.year,
                month=bday.month,
                day=bday.day
            ).date()

            if birthday_this_year < today_date:
                next_birthday = datetime(
                    year=today_date.year + 1,
                    month=bday.month,
                    day=bday.day
                ).date()
            else:
                next_birthday = birthday_this_year

            diff_days = (next_birthday - today_date).days

            if 0 <= diff_days <= days:
                congratulation_date = next_birthday

                if congratulation_date.weekday() == 5:  
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                congratulation_users.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })

        return congratulation_users
