"""
Module for validating the transfer type for money transfer operations.

Ensures that the transfer type is one of the accepted values: "ORDINARY", "INMEDIATE", or "URGENT".
Raises a validation exception if the provided type is invalid.
"""
from uc3m_money.data.attr.attribute import Attribute

class TransferType(Attribute):
    """
    TransferType class for validating the type of a money transfer.

    Inherits from Attribute and checks that the transfer type matches
    one of the allowed options: "ORDINARY", "INMEDIATE", or "URGENT".

    Attributes:
        _validation_pattern (str): Regular expression for allowed transfer types.
        _error_message (str): Error message if validation fails.
        _attr_value (str): Validated transfer type.
    """
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._error_message = "Invalid transfer type"
        self._attr_value = self._validate(attr_value)
