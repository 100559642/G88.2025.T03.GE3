"""Account manager module """
import json
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)
from uc3m_money.data.attr.iban_code import IbanCode
from uc3m_money.iban_balance import IbanBalance
from uc3m_money.storage.transfer_json_store import TransferJsonStore
from uc3m_money.storage.deposits_json_store import DepositsJsonStore
from uc3m_money.storage.balances_json_store import BalancesJsonStore


from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""

        my_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)
        transfers_storage = TransferJsonStore()
        transfers_storage.adding_item(my_request)

        return my_request.transfer_code


    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        deposit_obj = AccountDeposit.load_deposit_from_file(input_file)

        deposits_storage = DepositsJsonStore()
        deposits_storage.adding_item(deposit_obj)
        return deposit_obj.deposit_signature

    def read_transactions_file(self):
        """loads the content of the transactions file
        and returns a list"""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return input_list


    def calculate_balance(self, iban:str)->bool:
        """calculate the balance for a given iban"""
        iban = IbanCode(iban).value
        iban_balance = IbanBalance(iban)
        balances_storage = BalancesJsonStore()
        balances_storage.adding_item(iban_balance)
        return True
