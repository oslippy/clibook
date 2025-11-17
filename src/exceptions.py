"""Custom exception classes for CLI validation and domain errors."""


class AddressBookError(Exception):
    """Base exception for address book errors."""


class RecordNotFoundError(LookupError):
    """Raised when a contact/record is not found."""


class InvalidInputError(ValueError):
    """Raised when CLI input is syntactically incorrect."""


class InvalidNameError(ValueError):
    """Raised when a name is empty or invalid."""


class InvalidPhoneError(ValueError):
    """Raised when a phone number cannot be parsed or is invalid."""


class PhoneNotFoundError(LookupError):
    """Raised when a phone number is not present in a record."""


class InvalidBirthdayError(ValueError):
    """Raised for invalid birthday formats or future dates."""


class InvalidEmailError(ValueError):
    """Raised when an email has invalid format."""


class EmailNotFoundError(LookupError):
    """Raised when an email is not present in a record."""


class InvalidAddressError(ValueError):
    """Raised when an address is empty or otherwise invalid."""


class InvalidSearchQueryError(ValueError):
    """Raised when a search query is empty."""


class InvalidDaysError(ValueError):
    """Raised when days parameter is negative."""


class EditCommandNotFound(ValueError):
    """Raised when an unsupported field is provided to the edit command."""


class AddressBookError(ValueError):
    pass


class InvalidNameError(ValueError):
    """Raised when a name is empty or invalid."""
    pass


class InvalidPhoneError(ValueError):
    """Raised when a phone number cannot be parsed or is invalid."""
    pass


class RecordNotFoundError(ValueError):
    """Raised when a contact/record is not found."""
    pass


class DuplicateRecordError(ValueError):
    """Raised when trying to add a record that already exists."""
    pass


class PhoneNotFoundError(ValueError):
    """Raised when a phone number is not present in a record."""
    pass


class InvalidBirthdayError(ValueError):
    """Raised for invalid birthday formats or future dates."""
    pass


class InvalidEmailError(ValueError):
    """Raised when an email has invalid format."""
    pass


class EmailNotFoundError(ValueError):
    """Raised when an email is not present in a record."""
    pass


class InvalidAddressError(ValueError):
    """Raised when an address is empty or otherwise invalid."""
    pass


class InvalidSearchQueryError(ValueError):
    """Raised when a search query is empty."""
    pass


class InvalidInputError(ValueError):
    """Raised when CLI input is syntactically incorrect."""
    pass


class InvalidDaysError(ValueError):
    """Raised when days parameter is negative."""
    pass


class EditCommandNotFound(ValueError):
    """Raised when an unsupported field is provided to the edit command."""
    pass
