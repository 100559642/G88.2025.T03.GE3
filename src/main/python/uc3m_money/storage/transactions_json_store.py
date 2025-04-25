"""
Module for managing the storage of transfer transactions.

Defines the TransactionsJsonStore class, which handles saving and loading
transfer data to and from a JSON file with duplicate checking.
"""
from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE
from uc3m_money.storage.json_store import JsonStore


class TransactionsJsonStore(JsonStore):
    """
    TransactionsJsonStore class for handling transfer transaction storage.

    Inherits from JsonStore and sets the file label to the transactions
    store file. Manages operations related to saving and loading transfer data.

    Attributes:
        _file_label (str): Path to the JSON file used for storing transactions.
    """
    _file_label = TRANSACTIONS_STORE_FILE
