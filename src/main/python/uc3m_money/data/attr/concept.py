"""
Module for validating the concept field of a money transfer.

Ensures that the concept is between 10 and 30 characters long,
consists only of letters and spaces, and contains at least two words.
"""
from uc3m_money.data.attr.attribute import Attribute

class Concept(Attribute):
    """
    Concept class for validating the concept description of a transfer.

    Inherits from Attribute and checks that the concept:
    - Has between 10 and 30 characters.
    - Consists of alphabetic characters and spaces only.
    - Contains at least two words.

    Attributes:
        _validation_pattern (str): Regular expression enforcing format requirements.
        _error_message (str): Error message if validation fails.
        _attr_value (str): Validated concept string.
    """
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid concept format"
        self._attr_value = self._validate(attr_value)
