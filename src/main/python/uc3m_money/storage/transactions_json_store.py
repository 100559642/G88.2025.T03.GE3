from uc3m_money import AccountManagementException
from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE
from uc3m_money.storage.json_store import JsonStore

class TransferJsonStore(JsonStore):
    """class for handling Transfer Json"""
    _file_label = TRANSACTIONS_STORE_FILE
    def __init__(self):
        """constructor"""
        self._data_list = self.load_list_from_file()

    def adding_item(self, next_transfer):
        self.load_list_from_file()
        for existing_transfer in self._data_list:
            if existing_transfer == next_transfer.to_json():
                raise AccountManagementException("Duplicated transfer in transfer_list")
            super().adding_item(next_transfer)