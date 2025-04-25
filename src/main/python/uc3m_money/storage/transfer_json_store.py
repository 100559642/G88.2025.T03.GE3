"""
Module for managing the storage of money transfers.

Provides the TransferJsonStore class for adding, validating,
and storing transfer records in a JSON file, ensuring no duplicates are allowed.
"""
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import TRANSFERS_STORE_FILE

class TransferJsonStore(JsonStore):
    """subclass handling transfers"""
    _file_label = TRANSFERS_STORE_FILE

    def adding_item(self, item):
        for existing_transfer in self._data_list:
            if existing_transfer == item.to_json():
                raise AccountManagementException("Duplicated transfer in transfer list")
        super().adding_item(item)
