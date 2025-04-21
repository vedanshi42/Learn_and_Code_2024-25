import json
from account import Account
from card import Card


def load_account_data(filename="account_users.json"):
    try:
        with open(filename, "r") as file:
            user_data = json.load(file)
        
        accounts = []
        for user in user_data:
            # Create Account and Card objects for each user
            account = Account(
                account_number=user["account_number"],
                balance=user["balance"],
                daily_limit=user["daily_limit"]
            )
            card = Card(
                card_number=user["card_number"],
                pin=user["pin"]
            )
            accounts.append((user["name"], account, card)) 
        return accounts
    
    except FileNotFoundError as fileError:
        print(f"Error: {fileError}")

    except json.JSONDecodeError as jsonError:
        print(f"Error: {jsonError}")
    
    except Exception as e:
        raise e
