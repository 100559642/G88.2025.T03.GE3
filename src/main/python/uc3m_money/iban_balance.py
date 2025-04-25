import json
from uc3m_money.account_management_config import BALANCES_STORE_FILE, TRANSACTIONS_STORE_FILE
from uc3m_money.account_management_exception import AccountManagementException
from datetime import datetime, timezone

from uc3m_money.data.attr.iban_code import IbanCode


class IbanBalance:
    """Class to manage IBAN balances"""
    def __init__(self, iban: str):
        self.iban = IbanCode(iban).value

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

    def calculate_balance(self):
        """
                Calculates the balance for the provided IBAN by loading transactions
                or existing balance from the file.
                """
        transaction_list = self.read_transactions_file()
        iban_found = False
        balance = 0
        for transaction in transaction_list:
            # print(transaction["IBAN"] + " - " + iban)
            if transaction["IBAN"] == self.iban:
                balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return balance

    def to_json(self):
        """Returns the balance data in a JSON-compatible format."""
        return {
            "IBAN": self.iban,
            "time": datetime.timestamp(datetime.now(timezone.utc)),
            "BALANCE": self.calculate_balance()  # Get the calculated balance for the IBAN
        }