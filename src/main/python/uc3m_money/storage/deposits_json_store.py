"""module to handle deposit-related JSON file"""
from uc3m_money.storage.json_store import JsonStore
from uc3m_money.account_management_config import DEPOSITS_STORE_FILE

class DepositsJsonStore(JsonStore):
    """subclass to handle depositing json"""
    _file_label = DEPOSITS_STORE_FILE
