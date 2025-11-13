import re
from collections import UserDict
from datetime import datetime, timedelta
from typing import Any, Dict, List

from .exceptions import (
    InvalidBirthdayError,
    InvalidEmailError,
    InvalidNameError,
    InvalidPhoneError,
    PhoneNotFoundError,
    RecordNotFoundError,
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
        if not self._validate_phone(value):
            raise InvalidPhoneError(
                "You have entered an invalid number. A phone number must contain 10 digits."
            )
        super().__init__(value)

    @staticmethod
    def _validate_phone(phone_number: str) -> bool:
        pattern = re.compile(r"^\d{10}$")
        return bool(pattern.match(phone_number))


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
            raise ValueError("Address cannot be empty.")
        super().__init__(value.strip())


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = None
        self.birthday = None

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
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        raise PhoneNotFoundError(f"Phone {phone} not found in record.")

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self):
        parts = [f"Contact name: {self.name.value}"]
        if self.phones:
            parts.append(f"phones: {'; '.join(p.value for p in self.phones)}")
        if self.emails:
            parts.append(f"emails: {'; '.join(e.value for e in self.emails)}")
        if self.address:
            parts.append(f"address: {self.address.value}")
        return ", ".join(parts)


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

    @property
    def is_empty(self) -> bool:
        return not bool(self.data)

    @property
    def records(self) -> Dict[str, Any]:
        return self.data

    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        today_date = datetime.now().date()
        congratulation_users = []

        for record in self.data.values():
            if record.birthday is not None:
                if (
                    record.birthday.value.month == today_date.month
                    and today_date.day <= record.birthday.value.day
                    and (record.birthday.value.day - today_date.day) <= 7
                ):
                    birthday_current_year = datetime(
                        year=today_date.year,
                        month=record.birthday.value.month,
                        day=record.birthday.value.day,
                    )
                    congratulation_date = None
                    if birthday_current_year.weekday() in range(0, 5):
                        congratulation_date = birthday_current_year
                    elif birthday_current_year.weekday() == 5:
                        congratulation_date = birthday_current_year + timedelta(days=2)
                    else:
                        congratulation_date = birthday_current_year + timedelta(days=1)
                    congratulation_user = {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                    congratulation_users.append(congratulation_user)

        return congratulation_users
