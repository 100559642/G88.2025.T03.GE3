import json

from uc3m_money.account_management_exception import AccountManagementException


class JsonStore():
    """json store class"""
    _data_list = []
    _file_label = ""
    def __init__(self):
        self.load_list_from_file()
    def save_list_to_file(self):
        """saves the list in the store"""
        try:
            with open(self._file_label, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
    def load_list_from_file(self):
        """load list of items form store"""
        try:
            with open(self._file_label, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
    def adding_item(self, item):
        """add a new item to store"""
        self.load_list_from_file()
        self._data_list.append(item.to_json())
        self.save_list_to_file()

    def get_data_list(self):
        return self._data_list