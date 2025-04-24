"""Account manager module """
import re
import json
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_management_config import (TRANSFERS_STORE_FILE,
                                        DEPOSITS_STORE_FILE,
                                        TRANSACTIONS_STORE_FILE,
                                        BALANCES_STORE_FILE)

from uc3m_money.transfer_request import TransferRequest
from uc3m_money.account_deposit import AccountDeposit


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def valivan(iban_code: str):
        """
    Calcula el dígito de control de un IBAN español.

    Args:
        iban_code (str): El IBAN sin los dos últimos dígitos (dígito de control).

    Returns:
        str: El dígito de control calculado.
        """
        regex_ib = re.compile(r"^ES[0-9]{22}")
        regex_matches = regex_ib.fullmatch(iban_code)
        if not regex_matches:
            raise AccountManagementException("Invalid IBAN format")
        iban = iban_code
        original_code = iban[2:4]
        #replacing the control
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]


        # Convertir el IBAN en una cadena numérica, reemplazando letras por números
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')

        # Mover los cuatro primeros caracteres al final

        # Convertir la cadena en un número entero
        int_iban = int(iban)

        # Calcular el módulo 97
        iban_mod = int_iban % 97

        # Calcular el dígito de control (97 menos el módulo)
        control_digit = 98 - iban_mod

        if int(original_code) != control_digit:
            #print(control_digit)
            raise AccountManagementException("Invalid IBAN control digit")

        return iban_code

    def validate_concept(self, concept: str):
        """regular expression for checking the minimum and maximum length as well as
        the allowed characters and spaces restrictions
        there are other ways to check this"""
        regex_concept = re.compile(r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$")

        match_regex = regex_concept.fullmatch(concept)
        if not match_regex:
            raise AccountManagementException ("Invalid concept format")

    def validate_transfer_date(self, transfer_date):
        """validates the arrival date format  using regex"""
        regex_date = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        match_regex = regex_date.fullmatch(transfer_date)
        if not match_regex:
            raise AccountManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(transfer_date, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise AccountManagementException("Invalid date format")
        return transfer_date
    #pylint: disable=too-many-arguments
    def transfer_request(self, from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """first method: receives transfer info and
        stores it into a file"""
        self.valivan(from_iban)
        self.valivan(to_iban)
        self.validate_concept(concept)
        self.validate_transfer_type(transfer_type)
        self.validate_transfer_date(date)
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

    def validate_transfer_type(self, transfer_type):
        regex_type = re.compile(r"(ORDINARY|INMEDIATE|URGENT)")
        match_regex = regex_type.fullmatch(transfer_type)
        if not match_regex:
            raise AccountManagementException("Invalid transfer type")

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
        input_deposit = self.load_json_store(input_file)

        # comprobar valores del fichero
        try:
            deposit_iban = input_deposit["IBAN"]
            deposit_amount = input_deposit["AMOUNT"]
        except KeyError as e:
            raise AccountManagementException("Error - Invalid Key in JSON") from e


        deposit_iban = self.valivan(deposit_iban)
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
        iban = self.valivan(iban)
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
