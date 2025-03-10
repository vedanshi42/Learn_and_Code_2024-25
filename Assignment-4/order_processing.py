class OrderProcessing:
    def __init__(self):
        self.orders = []

    def process_order(self, user, item, quantity, price):
        total = self.calculate_total(quantity, price)
        self.add_order(item, quantity, total)
        self.print_order_details(user, item, quantity, total)
        
        if quantity > 10:
            self.bulk_order_alert()
        
        self.send_order_confirmation(user.email, item, total)

        return total

    def calculate_total(self, quantity, price):
        total = quantity * price
        if quantity > 5:
            total *= 0.85  # 15% discount
        return total

    def add_order(self, item, quantity, total):
        self.orders.append(f"Item: {item}, Qty: {quantity}, Total: {total}")

    def print_order_details(self, user, item, quantity, total):
        print("Order Placed!")
        print(f"User: {user.name}, Item: {item}, Quantity: {quantity}, Total: {total}")

    def bulk_order_alert(self):
        print("Bulk Order Alert!")

    def send_order_confirmation(self, email, item, total):
        self.send_email(email, f"Order placed for {item} with total cost {total}")

    def send_email(self, email, message):
        print(f"Sending email to: {email} | Message: {message}")
