class Card:
    def __init__(self, card_number: str, pin: str):
        self.__card_number = card_number
        self.__pin = pin
        self.invalid_attempts = 0
        self.__is_blocked = False

    def validate_pin(self, entered_pin: str) -> bool:
        if self.__is_blocked:
            raise ValueError("Card is blocked due to 3 invalid pin attempts")

        if entered_pin != self.__pin or len(str(entered_pin)) != 4:
            self.invalid_attempts += 1
            if self.invalid_attempts >= 3:
                self.__is_blocked = True
            return False

        self.invalid_attempts = 0
        return True

    def is_blocked(self) -> bool:
        return self.__is_blocked
