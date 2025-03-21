class PaymentService:
    def __init__(self, wallet):
        self.__wallet = wallet  # Wallet is private to payment Service

    def __can_pay(self, payment):  # can_pay is private method of this class
        return self.__wallet.get_current_balance() >= payment

    def process_payment(self, payment):
        if self.__can_pay(payment):
            self.__wallet.debit_amount(payment)
            return True
        return False
