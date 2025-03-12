class PaymentProcessing:
    def handle_payment(self, card_type, amount, card_name, card_number):
        if not self.validate_card_type(card_type):
            print("Unknown Payment Method")
            return
        
        self.process_transaction(card_type, amount)
        if amount > 1000:
            self.high_value_alert()
        
        self.confirm_payment(card_name, card_number)

    def validate_card_type(self, card_type):
        valid_types = ["credit", "debit"]
        return card_type.lower() in valid_types

    def process_transaction(self, card_type, amount):
        card_type = card_type.capitalize()
        print(f"Processing {card_type} Card payment of ${amount}")

    def high_value_alert(self):
        print("High-value transaction alert!")

    def confirm_payment(self, card_name, card_number):
        print(f"Payment Done for {card_name} (Card Ending: {card_number[-4:]})")
