"""
Module for validating transfer amounts for money transfers.

Ensures that the amount is a valid float, has no more than two decimal places,
and falls within the allowed range of 10 to 10,000 inclusive.
"""
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.data.attr.attribute import Attribute

class TransferAmount(Attribute):
    """
       TransferAmount class for validating the amount of a money transfer.

       Inherits from Attribute and validates that the transfer amount:
       - Is a float.
       - Has no more than two decimal places.
       - Is between 10 and 10,000 inclusive.

       Attributes:
           _error_message (str): Error message shown if validation fails.
           _attr_value (float): The validated transfer amount.
       """
    def __init__(self, attr_value):
        super().__init__()
        self._error_message = "Invalid transfer amount"
        self._attr_value = self._validate(attr_value)

    def _validate(self,attr_value):
        #attr_value = super()._validate(attr_value)
        try:
            float_amount = float(attr_value)
        except ValueError as exc:
            raise AccountManagementException("Invalid transfer amount") from exc
        string_amount = str(float_amount)
        if '.' in string_amount:
            decimales = len(string_amount.split('.')[1])
            if decimales > 2:
                raise AccountManagementException("Invalid transfer amount")
        if float_amount < 10 or float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")
        return float_amount
