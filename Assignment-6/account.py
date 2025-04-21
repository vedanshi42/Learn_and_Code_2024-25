class Account:
    def __init__(self, account_number, balance, daily_limit):
        self.__account_number = account_number  # Encapsulated account details
        self.__balance = balance
        self.__daily_limit = daily_limit
        self.__total_withdrawn_today = 0

    def get_balance(self):
        return self.__balance

    def debit(self, amount):
        if amount > self.__balance:
            return False
        else:
            self.__balance -= amount
            return True

    def can_withdraw(self, amount):
        if amount + self.__total_withdrawn_today > self.__daily_limit:
            return False
        return True

    def update_daily_withdrawn(self, amount):
        self.__total_withdrawn_today += amount

    def reset_daily_withdrawn(self):
        self.__total_withdrawn_today = 0
