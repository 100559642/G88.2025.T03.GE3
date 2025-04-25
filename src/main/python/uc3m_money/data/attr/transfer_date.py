"""
Module for validating transfer dates in money transfer operations.

Defines the TransferDate class, which ensures that a date is in the
correct format, is not in the past, and falls between the years 2025 and 2050.
"""
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.data.attr.attribute import Attribute

class TransferDate(Attribute):
    """
    TransferDate class for validating the date of a money transfer.

    Inherits from Attribute and checks that:
    - The date is in dd/mm/yyyy format.
    - The date is today or later.
    - The year is between 2025 and 2050.

    Attributes:
        _validation_pattern (str): Regex pattern to check date format.
        _error_message (str): Error message shown when validation fails.
        _attr_value (str): The validated transfer date string.
    """
    def __init__(self, attr_value):
        """
        Initialize a TransferDate by validating the provided date string.

        Args:
            attr_value (str): The transfer date to validate.

        Raises:
            AccountManagementException: If the date format is invalid,
            the date is in the past, or the year is out of range.
        """
        super().__init__()
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message = "Invalid date format"
        self._attr_value = self._validate(attr_value)

    def _validate(self,attr_value):
        """
        Validate the transfer date against format and logical rules.

        Args:
            attr_value (str): The transfer date string.

        Returns:
            str: The validated date string.

        Raises:
            AccountManagementException: If validation fails.
        """
        attr_value = super()._validate(attr_value)
        #transfer_date = attr_value
        try:
            my_date = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return attr_value
