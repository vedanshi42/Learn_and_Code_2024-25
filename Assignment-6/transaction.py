class Transaction:
    def __init__(self, account, card):
        self.account = account
        self.card = card

    def withdraw(self, amount):
        try:
            if self.card.is_blocked():
                raise ValueError("Card is blocked. Cannot proceed with the transaction.")

            if not self.account.can_withdraw(amount):
                raise ValueError("Withdrawal exceeds daily limit.")

            if self.account.debit(amount):
                self.account.update_daily_withdrawn(amount)
            else:
                raise ValueError('Insufficient Balance in account.')
            
            return True
        except ValueError as e:
            print(f"Error: Transaction failed - {e}")

    def reset_daily_limit(self):
        try:
            self.account.reset_daily_withdrawn()
            return True
        except Exception as e:
            print(f"Error: Failed to reset withdrawal limit - {e}")
