import msvcrt
import re


class UIHelpers:
    @staticmethod
    def get_hidden_password(prompt="Password: "):
        print(prompt, end='', flush=True)
        password = ''
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:
                print('')
                break
            elif ch == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            elif ch == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt
            else:
                try:
                    char = ch.decode('utf-8')
                except Exception:
                    continue
                password += char
                print('*', end='', flush=True)
        return password

    @staticmethod
    def is_valid_email(email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.(com|in|org|net|edu)$", email)
