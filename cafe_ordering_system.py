from datetime import date # Import class for the order date
from typing import List    # Import List type hint

# this class shows the implementation of the Observer Pattern
class Observer:
    """Observer interface. Any class that wants to receive notifications implements this."""
    def update(self, message: str):
        pass # Added by the observer for update method

class Subject:
    """Keeps a list of observers and notifies them of changes made."""
    def __init__(self):
        self._observers: List[Observer] = [] # List of attached observers

    def attach(self, observer: Observer):
        """this will add an observer to the list."""
        self._observers.append(observer) # Adds observer to the list

    def notify(self, message: str):
        """this will send a notification to all observers about any changes."""
        for observer in self._observers:  
            observer.update(message) # Observer is updated with the message

class OrderObserver(Observer):
    """Observer that prints notifications when orders are updated."""
    def update(self, message: str):
        print(f"[Notification] {message}") # Prints notification to the terminal

# Adding the factory pattern within the menu item
class MenuItemFactory:
    """Factory class for creating menu items."""
    @staticmethod
    def create_menu_item(item_type: str, item_id: int, name: str, price: float, size: str = None):
        """Create a FoodItem or DrinkItem based on type."""
        if item_type.lower() == "food":
            return FoodItem(item_id, name, price) # Creates FoodItem
        elif item_type.lower() == "drink":
            return DrinkItem(item_id, name, price, size) # Creates DrinkItem
        else:
            raise ValueError("Invalid menu item type") # Prints the error for invalid type by the user

# The classes for menu items
class MenuItem:
    """Base class for all menu items."""
    def __init__(self, item_id: int, item_name: str, item_price: float):
        self.item_id = item_id # Stores item ID
        self.item_name = item_name # Stores item name
        self.item_price = item_price # Stores item price

class FoodItem(MenuItem):
    """Represents food items."""
    def __init__(self, item_id: int, item_name: str, item_price: float):
        super().__init__(item_id, item_name, item_price) 

class DrinkItem(MenuItem):
    """Represents drink items with a size attribute."""
    def __init__(self, item_id: int, item_name: str, item_price: float, drink_size: str):
        super().__init__(item_id, item_name, item_price) 
        self.drink_size = drink_size  # Stores size of the drink

# This class shows a single item in a customer's order
class OrderItem:
    """Represents a single item in a customer's order."""
    def __init__(self, orderitem_id: int, menu_item: MenuItem, quantity: int):
        self.orderitem_id = orderitem_id  # Unique ID for order item
        self.menu_item = menu_item # Reference to MenuItem object
        self.quantity = quantity # Quantity ordered

    def get_line_total(self) -> float:
        """Calculate total the total cost."""
        return self.menu_item.item_price * self.quantity  # Price * Quantity

# This class shows the customer's full order containing multiple items
class Order(Subject):
    """Shows the customer's full order containing multiple items."""
    TAX_RATE = 0.20  # VAT rate

    def __init__(self, order_id: int, order_date: date, order_status: str):
        super().__init__() 
        self.order_id = order_id # Stores order ID
        self.order_date = order_date # Stores order date
        self.order_status = order_status # Stores order status
        self.order_items: List[OrderItem] = [] # List to store items in the order

    def add_item(self, order_item: OrderItem):
        self.order_items.append(order_item) # Add item to the order
        self.notify("Item added to order") # Notify observers

    def remove_item(self, list_number: int, qty: int):
        index = list_number - 1  
        if 0 <= index < len(self.order_items):  # Checks if valid index
            order_item = self.order_items[index] # Gets the order item
            if qty >= order_item.quantity: 
                self.order_items.pop(index)
                self.notify("Item has been removed from your order") # Notification for the removal of the item
            else: # Reduces quantity when the amount wanting to remove is less than the existing quantity
                order_item.quantity -= qty
                self.notify("the item quantity has been updated") # Notification for the update of the item quantity

    def get_total(self) -> float:
        try:
            subtotal = sum(item.get_line_total() for item in self.order_items) # Shows the subtotal
            return subtotal + subtotal * Order.TAX_RATE # Add VAT 
        except Exception as e:
            print(f"there was an error calculating the total: {e}") # Error handling 
            return 0.0

    def display_order(self):
        if not self.order_items:
            print("\nOrder is currently empty.\n") # Shows empty message
            return
        print("\nYour order:") # Prints the header
        for i, item in enumerate(self.order_items, start=1): # Lists all items
            if isinstance(item.menu_item, DrinkItem):
                # Show drink with size
                print(f"{i}. {item.menu_item.item_name} ({item.menu_item.drink_size}) x{item.quantity} - £{item.get_line_total():.2f}")
            else:
                # Shows food items
                print(f"{i}. {item.menu_item.item_name} x{item.quantity} - £{item.get_line_total():.2f}")
        print(f"Order Total (including VAT): £{self.get_total():.2f}\n") # Shows total

# The classes for customer and staff
class Customer:
    """Shows a customer placing an order."""
    def __init__(self, customer_id: int, customer_name: str):
        self.customer_id = customer_id # Stores customer ID
        self.customer_name = customer_name # Stores customer name

    def place_order(self, order: Order):
        if not order.order_items:
            print("Cannot place an empty order. Add items first.") # Error for empty order
        else:
            print(f"\nOrder {order.order_id} placed by {self.customer_name}") # Show confirmation
            print("Order completed successfully!\n")

class Staff:
    """Represents cafe staff responsibilities for updating order status."""
    def __init__(self, staff_id: int, staff_name: str):
        self.staff_id = staff_id # Staff ID
        self.staff_name = staff_name # Staff name

    def update_order_status(self, order: Order, new_status: str):
        order.order_status = new_status # Update order status
        order.notify(f"Order status updated to '{new_status}'") # Notify observers

# The classes for bill and payment
class Bill:
    """Generates a simple text-based bill for an order."""
    def __init__(self, bill_id: int, order: Order):
        self.bill_id = bill_id # Bill ID
        self.order = order # Associated order
        self.bill_total = order.get_total() # Total amount

    def generate_bill(self):
        print("\n===== Cafe Bill =====") # Header for the bill
        print(f"Bill ID: {self.bill_id}") # Prints bill ID
        print(f"Order ID: {self.order.order_id}") # Prints order ID
        print(f"Date: {self.order.order_date.strftime('%d/%m/%Y')}") # Prints order date
        print("---------------------")
        for item in self.order.order_items:  # Repeats items ordered
            line = item.menu_item.item_name
            if isinstance(item.menu_item, DrinkItem):
                line += f" ({item.menu_item.drink_size})" # Includes drink size
            line += f" x{item.quantity} - £{item.get_line_total():.2f}" # Includes quantity & total
            print(line)
        print("---------------------")
        print(f"Total (including VAT): £{self.bill_total:.2f}") # Shows total with VAT
        print("=====================\n") # Footer for the bill

class Payment:
    """Handles bill payment processing."""
    def __init__(self, payment_id: str, payment_method: str, payment_amount: float):
        self.payment_id = payment_id # Payment ID
        self.payment_method = payment_method # Cash or Card
        self.payment_amount = payment_amount # Amount that needs to be paid

    def process_payment(self):
        if self.payment_amount <= 0:
            print("Invalid payment amount. Cannot process payment.")  # Check for invalid amount
            return

        # Error handling: ask repeatedly until valid input is given
        while self.payment_method.upper() not in ["CASH", "CARD"]:
            self.payment_method = input("Invalid payment method. Please enter 'Cash' or 'Card': ")

        print(f"Payment of £{self.payment_amount:.2f} received via {self.payment_method}") # Shows confirmation

# Class for menu management
class Menu:
    """Stores all menu items and allows add/remove/display operations."""
    def __init__(self):
        self.items: List[MenuItem] = [] # List to store menu items

    def add_item(self, item: MenuItem):
        self.items.append(item) # Add item to menu

    def remove_item(self, item_id: int):
        # Removes item by ID
        self.items = [item for item in self.items if item.item_id != item_id]

    def display(self):
        if not self.items:
            print("Menu is empty.") # Shows this message if no items
            return
        print("\n===== Cafe Menu =====") # Header for the menu
        for item in self.items:
            if isinstance(item, FoodItem):
                print(f"{item.item_id}. {item.item_name} (£{item.item_price:.2f}) - Food") # Show food items
            else:
                print(f"{item.item_id}. {item.item_name} (£{item.item_price:.2f}) - Drink [{item.drink_size}]") # Shows drink
        print("=====================") # Footer for the menu

    def get_item_by_id(self, item_id: int):
        for item in self.items: # Searches for items
            if item.item_id == item_id:
                return item # Return if found
        return None  # Return None if not found

# Main script that interacts with the user
if __name__ == "__main__":
    menu = Menu() 
    # Add all menu items food and drinks
    menu.add_item(MenuItemFactory.create_menu_item("food", 1, "Chuna Sandwich", 3.50))
    menu.add_item(MenuItemFactory.create_menu_item("food", 2, "Chicken Wrap", 4.50))
    menu.add_item(MenuItemFactory.create_menu_item("food", 3, "Turkey Sandwich", 1.80))
    menu.add_item(MenuItemFactory.create_menu_item("drink", 4, "Latte", 2.80, "Medium"))
    menu.add_item(MenuItemFactory.create_menu_item("drink", 5, "Espresso", 2.20, "Small"))
    menu.add_item(MenuItemFactory.create_menu_item("drink", 6, "Diet Coke", 1.20, "Can"))
    menu.add_item(MenuItemFactory.create_menu_item("drink", 7, "Water", 0.80, "Bottle"))
    menu.add_item(MenuItemFactory.create_menu_item("drink", 8, "Flat White", 2.00, "Medium"))

    name = input("Enter your name: ") # Gets customer name
    customer = Customer(1, name) # Creates customer object

    order = Order(2, date.today(), "Pending") # Creates order object
    order.attach(OrderObserver()) # Attaches the observer
    order_item_counter = 1 # Order item counter

    # Main order loop
    while True:
        menu.display() # Displays menu
        choice = input("Enter the number of the item you want to order (or press Q to finish): ").strip()
        if choice.upper() == "Q": # Checks if user wants to finish
            order.display_order() # Shows current order
            if input("Confirm your order? (Y/N): ").upper() == "Y": # Confirms order
                break
            continue

        try:
            item = menu.get_item_by_id(int(choice)) # Gets selected item
            if not item:
                print("Invalid menu item number.")
                continue
            qty = int(input("Enter quantity of this item: ")) # Asks for quantity
            if qty <= 0:
                raise ValueError
            order.add_item(OrderItem(order_item_counter, item, qty)) # Adds to order
            order_item_counter += 1  # Adds order item ID
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

        # Optional removal loop
        while True:
            order.display_order() # Shows current order
            remove = input("Remove an item? (Y/N): ").upper() # Asks if they want to remove an item
            if remove != "Y":
                break
            try:
                remove_num = int(input("Enter the item number to remove from your current order: "))
                selected_item = order.order_items[remove_num - 1]
                remove_qty = int(input(f"Quantity to remove (max {selected_item.quantity}): "))
                if remove_qty <= 0:
                    raise ValueError
                order.remove_item(remove_num, remove_qty) # Removes items
            except (ValueError, IndexError):
                print("Invalid removal selection.") # Handles invalid input

    # Places order
    customer.place_order(order)

    # Staff updates order status
    staff = Staff(1, "Steve Jobs")
    staff.update_order_status(order, "Completed")

    # Generates bill and process payment
    bill = Bill(1, order)
    bill.generate_bill()
    payment_method = input("Enter payment method (Cash/Card): ")
    payment = Payment("PAY001", payment_method, bill.bill_total)
    payment.process_payment()
