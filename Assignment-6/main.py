from atm import ATM
from user_data_reader import load_account_data


def process_atm_transaction(user_name, amount):
    accounts = load_account_data()
    user_account = None
    user_card = None

    for name, account, card in accounts:
        if name == user_name:
            user_account = account
            user_card = card
            break

    if not user_account or not user_card:
        print(f"Error: User {user_name} not found.")
        return

    atm_machine = ATM(user_card, user_account)

    atm_machine.insert_card()
    if atm_machine.enter_pin(input('Enter ATM pin: ')):
        atm_machine.check_balance()
        atm_machine.withdraw_cash(amount)
    else:
        atm_machine.enter_pin(input('Enter pin again: '))


try:
    process_atm_transaction("Amit Sharma", 4000)
except Exception as e:
    print(f"Error processing transaction: {e}")
