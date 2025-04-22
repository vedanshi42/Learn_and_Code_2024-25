class Account:
    def __init__(self, account_number: str, balance: float, daily_limit: float):
        self.__account_number = account_number
        self.__balance = balance
        self.__daily_limit = daily_limit
        self.__total_withdrawn_today = 0

    def get_balance(self) -> float:
        return self.__balance

    def debit(self, amount: float) -> bool:
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    def can_withdraw(self, amount: float) -> bool:
        return (amount + self.__total_withdrawn_today) <= self.__daily_limit

    def update_daily_withdrawn(self, amount: float) -> None:
        self.__total_withdrawn_today += amount

    def reset_daily_withdrawn(self) -> None:
        self.__total_withdrawn_today = 0
