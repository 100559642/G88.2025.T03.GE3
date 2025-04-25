"""
Module for managing the storage of account balances.

Defines the BalancesJsonStore class, which handles saving and loading
account balance data to and from a JSON file.
"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import BALANCES_STORE_FILE

class BalancesJsonStore(JsonStore):
    """class for handling balances storage"""
    _file_label = BALANCES_STORE_FILE
