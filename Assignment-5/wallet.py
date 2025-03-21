class Wallet:
    def __init__(self, value=0.0):
        self.__value = value  # Making 'value' a private variable of Wallet

    def get_current_balance(self):
        return self.__value

    def _set_current_balance(self, new_balance):
        self.__value = new_balance

    def deposit_amount(self, deposit):
        self.__value += deposit

    def debit_amount(self, debit):
        self.__value -= debit
