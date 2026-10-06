class ConsoleView:
    @staticmethod
    def display_menu():
        print("\n=== FOOD ORDERING SYSTEM ===")
        print("1. Create (Place New Order)")
        print("2. Read (View All Orders)")
        print("3. Update (Modify Existing Order)")
        print("4. Delete (Cancel Order)")
        print("5. View Analytics Summary")
        print("6. View Analytics Chart (Graph)")
        print("0. Exit")

    @staticmethod
    def prompt_choice():
        return input("\nEnter choice: ").strip()

    @staticmethod
    def prompt_place_order():
        return input("Customer name: "), int(input("Item ID: ")), int(input("Quantity: "))

    @staticmethod
    def prompt_update_order():
        o_id = int(input("Enter Order ID to update: "))
        print("(Press Enter to keep current value)")
        c_name = input("New customer name: ").strip()
        item_id_str = input("New item ID: ").strip()
        qty_str = input("New quantity: ").strip()
        item_id = int(item_id_str) if item_id_str else None
        qty = int(qty_str) if qty_str else None
        return o_id, c_name, item_id, qty

    @staticmethod
    def prompt_delete_order():
        return int(input("Enter Order ID to delete: "))

    @staticmethod
    def display_orders(orders):
        if not orders:
            print("\nNo orders found.")
            return

        print("\n--- ORDERS LIST ---")
        for o in orders[:]:
            date_str = o['order_date'].strftime('%Y-%m-%d %H:%M') if o.get('order_date') else 'N/A'
            item_name = o.get('item_name') or f"Item #{o.get('item_id', 'N/A')}"

            print(f"Order ID: {o['order_id']} | Date: {date_str} | Customer: {o['customer_name']} | "
                  f"Item: {item_name} | Qty: {o['quantity']} | Total: ${o['total_price']:.2f}")

    @staticmethod
    def display_summary(summary):
        print("\n--- ANALYTICS SUMMARY ---")
        for k, v in summary.items():
            print(f"{k.replace('_', ' ').title()}: {v}")

    @staticmethod
    def display_message(msg):
        print(f"[SUCCESS]: {msg}")

    @staticmethod
    def display_error(error):
        print(f"[ERROR]: {error}")