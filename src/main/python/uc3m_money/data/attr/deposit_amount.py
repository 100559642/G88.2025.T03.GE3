"""
Module for validating deposit amounts in account management.

Provides the DepositAmount class to ensure that deposit amounts
are properly formatted and greater than zero.
"""
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.data.attr.attribute import Attribute

class DepositAmount(Attribute):
    """
    DepositAmount class for validating deposit amount fields.

    Inherits from Attribute and ensures that:
    - The amount follows the format "EUR XXXX.XX".
    - The numeric value of the deposit is greater than zero.

    Attributes:
        _validation_pattern (str): Regular expression to match the deposit format.
        _error_message (str): Error message shown if validation fails.
        _attr_value (float): The validated deposit amount.
    """
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._error_message = "Error - Invalid deposit amount"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        attr_value = super()._validate(attr_value)
        deposit_amount_float = float(attr_value[4:])
        if deposit_amount_float == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")
        return deposit_amount_float
