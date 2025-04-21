from transaction import Transaction


class ATM:
    def __init__(self, card, account):
        self.transaction = Transaction(account, card)

    def insert_card(self):
        print("Card inserted. Please enter your 4 digit PIN.")

    def enter_pin(self, entered_pin):
        try:
            if self.transaction.card.validate_pin(entered_pin):
                print("PIN validated successfully.")
                return True
            elif self.transaction.card.invalid_attempts < 3:
                new_pin = input('Enter pin again')
                self.transaction.card.validate_pin(new_pin)
            elif self.transaction.card.invalid_attempts >= 3:
                raise ValueError('Card blocked after 3 invalid attempts')
            else:
                raise ValueError('Enter numeric 4 digit pin')
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def withdraw_cash(self, amount):
        try:
            if amount > 0 and isinstance(amount, int):
                if self.transaction.withdraw(amount):
                    print(f"Successfully withdrawn {amount}")
                    print(f"Remaining balance: {self.transaction.account.get_balance()}")
            else:
                raise ValueError
        except ValueError as e:
            print(f"Error: Please enter the correct positive whole number amount to withdraw {e}")

        except ConnectionError as e:
            print(f"Error: Unable to connect to Server. {e}")

    def check_balance(self):
        try:
            print(f"Your current balance is: {self.transaction.account.get_balance()}")
        except ValueError as e:
            print(f'Error: {e}')
        except ConnectionError as e:
            print(f"Error: Unable to connect to Server. {e}")

    def reset_withdraw_limit(self):
        try:
            if self.transaction.reset_daily_limit():
                print("Daily withdrawal limit has been reset.")
        except Exception as e:
            print(f"Error: {e}")
