from atm import ATM
from user_data_reader import load_account_data


def process_atm_transaction(user_name: str, amount: int):
    try:
        accounts = load_account_data()
        user_account, user_card = None, None

        for name, account, card in accounts:
            if name == user_name:
                user_account, user_card = account, card
                break

        if not user_account or not user_card:
            raise ValueError(f"User {user_name} not found.")

        atm_machine = ATM(user_card, user_account)
        atm_machine.insert_card()

        for attempt in range(3):
            entered = input("Enter ATM PIN: ")
            if atm_machine.enter_pin(entered):1
                atm_machine.check_balance()
                atm_machine.withdraw_cash(amount)
                return
            else:
                print(f"Invalid PIN. Attempt {attempt + 1}/3")

        print("Maximum attempts reached. Card may be blocked.")

    except Exception as e:
        print(f"Error processing transaction: {e}")


if __name__ == "__main__":
    process_atm_transaction("Amit Sharma", 4000)
