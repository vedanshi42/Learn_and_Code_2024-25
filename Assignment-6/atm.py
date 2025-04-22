from transaction import Transaction


class ATM:
    def __init__(self, card, account):
        self.transaction = Transaction(account, card)

    def insert_card(self) -> None:
        print("Card inserted. Please enter your 4 digit PIN.")

    def enter_pin(self, entered_pin: str) -> bool:
        try:
            return self.transaction.card.validate_pin(entered_pin)
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def withdraw_cash(self, amount: int) -> None:
        if amount <= 0 or not isinstance(amount, int):
            print("Error: Please enter a positive whole number to withdraw.")
            return

        try:
            if self.transaction.withdraw(amount):
                print(f"Successfully withdrawn {amount}")
                print(f"Remaining balance: {self.transaction.account.get_balance()}")
        except ValueError as e:
            print(f"Transaction failed: {e}")

    def check_balance(self) -> None:
        print(f"Your current balance is: {self.transaction.account.get_balance()}")

    def reset_withdraw_limit(self) -> None:
        try:
            self.transaction.reset_daily_limit()
            print("Daily withdrawal limit has been reset.")
        except Exception as e:
            print(f"Error: {e}")
