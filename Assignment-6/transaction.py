class Transaction:
    def __init__(self, account, card):
        self.account = account
        self.card = card

    def withdraw(self, amount: float) -> bool:
        if self.card.is_blocked():
            raise ValueError("Card is blocked. Cannot proceed with the transaction.")

        if not self.account.can_withdraw(amount):
            raise ValueError("Withdrawal exceeds daily limit.")

        if not self.account.debit(amount):
            raise ValueError("Insufficient balance in account.")

        self.account.update_daily_withdrawn(amount)
        return True

    def reset_daily_limit(self) -> None:
        self.account.reset_daily_withdrawn()