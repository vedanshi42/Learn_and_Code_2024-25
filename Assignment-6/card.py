class Card:
    def __init__(self, card_number, pin):
        self.__card_number = card_number 
        self.__pin = pin
        self.invalid_attempts = 0
        self.__is_blocked = False

    def validate_pin(self, entered_pin):
        if self.__is_blocked:
            print('Card is blocked due to 3 invalid pin attempts')
            return False

        if entered_pin != self.__pin or len(str(entered_pin)) != 4:
            self.invalid_attempts += 1
            print("Invalid PIN. Enter correct 4 digit pin")

            if self.invalid_attempts >= 3:
                self.__is_blocked = True
            return False

        self.invalid_attempts = 0  # Reset invalid attempts after successful PIN entry
        return True

    def is_blocked(self):
        return self.__is_blocked
