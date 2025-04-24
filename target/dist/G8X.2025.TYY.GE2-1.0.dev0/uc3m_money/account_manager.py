"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)
from uc3m_money.data.attr.iban_code import IbanCode
from uc3m_money.data.attr.transfer_type import TransferType

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
        #IbanCode(from_iban)
        #IbanCode(to_iban)
        #self.validate_concept(concept)
        #TransferType.validate(transfer_type)
        #self.validate_transfer_date(date)
        self.validate_deposit_amount(amount)

        my_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)

        load_transfer = self.load_json_store(TRANSFERS_STORE_FILE)

        for existing_transfer in load_transfer:
            if (existing_transfer["from_iban"] == my_request.from_iban and
                    existing_transfer["to_iban"] == my_request.to_iban and
                    existing_transfer["transfer_date"] == my_request.transfer_date and
                    existing_transfer["transfer_amount"] == my_request.transfer_amount and
                    existing_transfer["transfer_concept"] == my_request.transfer_concept and
                    existing_transfer["transfer_type"] == my_request.transfer_type):
                raise AccountManagementException("Duplicated transfer in transfer list")

        load_transfer.append(my_request.to_json())

        try:
            with open(TRANSFERS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(load_transfer, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        return my_request.transfer_code

    def validate_deposit_amount(self, amount):
        try:
            float_amount = float(amount)
        except ValueError as exc:
            raise AccountManagementException("Invalid transfer amount") from exc
        string_amount = str(float_amount)
        if '.' in string_amount:
            decimales = len(string_amount.split('.')[1])
            if decimales > 2:
                raise AccountManagementException("Invalid transfer amount")
        if float_amount < 10 or float_amount > 10000:
            raise AccountManagementException("Invalid transfer amount")

    def load_json_store(self, input_f):
        try:
            with open(input_f, "r", encoding="utf-8", newline="") as file:
                load_transfer = json.load(file)
        except FileNotFoundError:
            load_transfer = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return load_transfer

    def deposit_into_account(self, input_file:str)->str:
        """manages the deposits received for accounts"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                input_deposit = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar valores del fichero
        try:
            deposit_iban = input_deposit["IBAN"]
            deposit_amount = input_deposit["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e


        deposit_iban = IbanCode(deposit_iban).value
        regex_amount = re.compile(r"^EUR [0-9]{4}\.[0-9]{2}")
        match_regex = regex_amount.fullmatch(deposit_amount)
        if not match_regex:
            raise AccountManagementException("Error - Invalid deposit amount")

        deposit_amount_float = float(deposit_amount[4:])
        if deposit_amount_float == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")

        deposit_obj = AccountDeposit(to_iban=deposit_iban,
                                     deposit_amount=deposit_amount_float)
        deposit_lists = self.load_json_store(DEPOSITS_STORE_FILE)

        deposit_lists.append(deposit_obj.to_json())

        try:
            with open(DEPOSITS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(deposit_lists, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

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
        transaction_list = self.read_transactions_file()
        iban_found = False
        balance = 0
        for transaction in transaction_list:
            #print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == iban:
                balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")

        last_balance = {"IBAN": iban,
                        "time": datetime.timestamp(datetime.now(timezone.utc)),
                        "BALANCE": balance}
        balance_list = self.load_json_store(BALANCES_STORE_FILE)
        balance_list.append(last_balance)

        try:
            with open(BALANCES_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(balance_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file  or file path") from ex
        return True
