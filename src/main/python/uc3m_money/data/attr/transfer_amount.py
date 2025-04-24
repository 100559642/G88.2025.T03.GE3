from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.data.attr.attribute import Attribute

class TransferAmount(Attribute):
    def __init__(self, attr_value):
        #self._validation_pattern = r""
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
