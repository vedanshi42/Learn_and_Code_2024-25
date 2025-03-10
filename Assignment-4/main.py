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
    order_processor.process_order(user, ordered_item, count_of_ordered_items, price_of_each_item)

    payment_processor = PaymentProcessing()

    total_payment_requested = count_of_ordered_items * price_of_each_item
    payment_processor.handle_payment("Credit", total_payment_requested, username, "1234567812345678")


if __name__ == "__main__":
    main()
