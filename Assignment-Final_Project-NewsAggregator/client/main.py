from client.ui.auth_ui import AuthUI
from client.ui.user_ui import UserUI
from client.ui.admin_ui import AdminUI


def home_screen():
    while True:
        print("\n=== Welcome to NewsViews ===")
        print("1. Login\n2. Signup\n3. Exit")
        user_choice = input("Choose: ")
        auth = AuthUI()
        if user_choice == '1':
            user = auth.login()
        elif user_choice == '2':
            user = auth.signup()
        elif user_choice == '3':
            break
        else:
            continue

        if user:
            if user['role'] == 'admin':
                AdminUI().menu()
            else:
                UserUI().menu(user)


if __name__ == "__main__":
    try:
        home_screen()
    except Exception as e:
        print(f'Error: Failed to login/create the user {e}')
