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
    pass


class InvalidPhoneError(ValueError):
    pass


class RecordNotFoundError(ValueError):
    pass


class DuplicateRecordError(ValueError):
    pass


class PhoneNotFoundError(ValueError):
    pass


class InvalidBirthdayError(ValueError):
    pass


class InvalidEmailError(ValueError):
    pass


class EmailNotFoundError(ValueError):
    pass


class InvalidAddressError(ValueError):
    pass


class InvalidSearchQueryError(ValueError):
    pass


class InvalidInputError(ValueError):
    pass

class InvalidDaysError(ValueError):
    pass

class EditCommandNotFound(ValueError):
    pass