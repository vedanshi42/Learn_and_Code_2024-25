class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def show_info(self):
        print(f"User Name: {self.name}, Email: {self.email}")
