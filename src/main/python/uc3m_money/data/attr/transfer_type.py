from uc3m_money.data.attr.attribute import Attribute
from uc3m_money.account_management_exception import AccountManagementException

class TransferType(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._error_message = "Invalid transfer type"
        self._attr_value = self._validate(attr_value)