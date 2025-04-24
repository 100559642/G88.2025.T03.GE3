import re
from uc3m_money.account_management_exception import AccountManagementException
class Attribute():
    """Attribute class definition"""
    def __init__(self):
        self._validation_pattern = r""
        self._error_message = ""
        self._attr_value = ""

    def _validate(self, attr_value):
        """Attribute validation"""
        specific_regex = re.compile(self._validation_pattern)
        match_regex = specific_regex.fullmatch(attr_value)
        if not match_regex:
            raise AccountManagementException(self._error_message)
        return attr_value
    @property
    def value(self):
        """returns attr value"""
        return self._attr_value
    @value.setter
    def value(self, attr_value):
        self._attr_value = self._validate(attr_value)

