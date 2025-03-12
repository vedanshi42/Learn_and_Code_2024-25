from user import User
from order_processing import OrderProcessing
from payment_processing import PaymentProcessing


def main():
    username = input("Enter name of user ")
    user_email = input('Enter user email-id (include @) ')

    user = User(username, user_email)

    ordered_item = input('Enter the item ordered ')
    count_of_ordered_items = int(input(f'Enter the number of {ordered_item} ordered '))
    price_of_each_item = int(input('Enter price for one item (number only) '))

    order_processor = OrderProcessing()
    total_payment_requested = order_processor.process_order(user, ordered_item, count_of_ordered_items, price_of_each_item)

    payment_method = input('Select a payment method (Credit or Debit Card) ')
    card_number = input(f"Enter {payment_method} card number ")

    payment_processor = PaymentProcessing()
    payment_processor.handle_payment(payment_method, total_payment_requested, username, card_number)


if __name__ == "__main__":
    main()
