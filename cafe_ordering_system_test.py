import unittest # Pythons built in unit testing framework
from datetime import date # Import date class for the order date

# Import the classes from the main system (cafe_ordering_system.py)
from cafe_ordering_system import (
    Menu,                           
    MenuItemFactory,                
    Order,                          
    OrderItem,                      
    OrderObserver                   
)


class CafeOrderingSystemTests(unittest.TestCase):
    """
    Unit tests for the cafe ordering system.
    These tests verify the core system components work correctly
    without requiring user input.
    """

    def setUp(self):
        """
        Runs before each test.
        Sets up a menu and an empty order ready for testing.
        """
        self.menu = Menu() # Creates a new menu for testing

        # Adds a food item to the menu using the factory pattern
        self.menu.add_item(
            MenuItemFactory.create_menu_item("food", 1, "Chuna Sandwich", 3.50)
        )

        # Adds a drink item to the menu using the factory pattern
        self.menu.add_item(
            MenuItemFactory.create_menu_item("drink", 2, "Latte", 2.80, "Medium")
        )

        # Creates a new order for testing
        self.order = Order(1, date.today(), "Pending")

        # Attaches an observer to mirror real system behaviour
        self.order.attach(OrderObserver())

    def test_add_item_to_order(self):
        """
        Test that adding an item increases order size
        and calculates the total correctly including VAT.
        """
        item = self.menu.get_item_by_id(1) # Retrieves an item from the menu
        self.order.add_item(OrderItem(1, item, 2)) # Adds 2 of that item to the order

        # Confirms that one item exists in the order
        self.assertEqual(len(self.order.order_items), 1)

        # Confirms that the total includes VAT 20%
        self.assertAlmostEqual(self.order.get_total(), 3.50 * 2 * 1.20)

    def test_remove_item_from_order(self):
        """
        Test that removing an item updates quantities
        and removes the item when quantity reaches zero.
        """
        item = self.menu.get_item_by_id(1) # Retrieves a menu item
        self.order.add_item(OrderItem(1, item, 3))  # Adds 3 items to the order

        # Removes 2 items and check remaining quantity
        self.order.remove_item(1, 2)
        self.assertEqual(self.order.order_items[0].quantity, 1)

        # Removes the final item and confirm the order is empty
        self.order.remove_item(1, 1)
        self.assertEqual(len(self.order.order_items), 0)

    def test_empty_order_total_is_zero(self):
        """
        Test that an empty order returns £0.00.
        """
        empty_order = Order(2, date.today(), "Pending") # Creates an empty order
        empty_order.attach(OrderObserver()) # Attaches observer

        # Confirms total is zero when no items exist in the order
        self.assertEqual(empty_order.get_total(), 0.0)

    def test_invalid_menu_item_lookup(self):
        """
        Test that requesting a non-existent menu item
        safely returns None.
        """
        # Attempts to retrieve an item ID that does not exist
        self.assertIsNone(self.menu.get_item_by_id(999))


# Run the unit tests
if __name__ == "__main__":
    unittest.main() 
