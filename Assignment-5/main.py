from customer import Customer
from wallet import Wallet
from payment_service import PaymentService


def main():
    first_name, last_name = input('Enter first and last name of the Customer (seperated by space): ').split(" ")

    customer_wallet = Wallet(100.0)  # Initial wallet balance is 100.0
    customer = Customer(first_name, last_name, customer_wallet)

    print(f"Welcome, {customer.get_first_name()} {customer.get_last_name()}.")
    print(f"Your current wallet balance is {customer.get_wallet()}")

    payment_service = PaymentService(customer_wallet)
    payment = float(input('Enter payment amount with decimal: '))

    if payment_service.process_payment(payment):
        print(f"Payment of {payment} completed successfully.")
        print(f"Updated wallet balance is {customer.get_wallet()}")
    else:
        print("Insufficient funds. Please try again later.")


if __name__ == "__main__":
    main()
