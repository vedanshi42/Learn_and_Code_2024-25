import msvcrt
import re
from datetime import datetime


class UIHelpers:
    @staticmethod
    def get_hidden_password(prompt="Password: "):
        print(prompt, end="", flush=True)
        password = ""
        while True:
            choice = msvcrt.getch()
            if choice in {b"\r", b"\n"}:
                print("")
                break
            elif choice == b"\x08":  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif choice == b"\x03":  # Ctrl+C
                raise KeyboardInterrupt
            else:
                try:
                    char = choice.decode("utf-8")
                except Exception:
                    continue
                password += char
                print("*", end="", flush=True)
        return password

    @staticmethod
    def is_valid_email(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.(com|in|org|net|edu)$", email)

    @staticmethod
    def validate_date_format(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"Invalid date format: '{date_str}'. Use YYYY-MM-DD.")
