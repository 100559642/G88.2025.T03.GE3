import json

from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import TRANSACTIONS_STORE_FILE
from uc3m_money.storage.json_store import JsonStore


class TransactionsJsonStore(JsonStore):
    """Class for handling Transfer JSON"""
    _file_label = TRANSACTIONS_STORE_FILE

