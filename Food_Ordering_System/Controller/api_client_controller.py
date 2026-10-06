from datetime import datetime
from Controller.database_controller import DatabaseController
from Controller.order_calculator_controller import OrderCalculatorController
from Model.schemas_model import FoodItemSchema, UpdateFoodItemSchema, OrderSchema, UpdateOrderSchema

class ApiClientController:
    def __init__(self):
        self.db_controller = DatabaseController()

    # --- FOOD ITEMS CRUD ---
    def create_food_item(self, item: FoodItemSchema):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO food_items (name, category, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (item.name.strip(), item.category.strip(), item.price))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"item_id": item_id, "name": item.name, "category": item.category, "price": item.price}

    def get_all_food_items(self):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM food_items")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def update_food_item(self, item_id: int, updates: UpdateFoodItemSchema):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM food_items WHERE item_id = %s", (item_id,))
        existing = cursor.fetchone()
        if not existing:
            cursor.close()
            conn.close()
            raise ValueError(f"Food Item ID {item_id} not found.")

        new_name = updates.name if updates.name is not None else existing['name']
        new_category = updates.category if updates.category is not None else existing['category']
        new_price = updates.price if updates.price is not None else existing['price']

        query = "UPDATE food_items SET name = %s, category = %s, price = %s WHERE item_id = %s"
        cursor.execute(query, (new_name, new_category, new_price, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Food Item {item_id} updated successfully."}

    def delete_food_item(self, item_id: int):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_items WHERE item_id = %s", (item_id,))
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise ValueError(f"Food Item ID {item_id} not found.")
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Food Item {item_id} deleted successfully."}

    # --- ORDERS CRUD ---
    def create_order(self, order: OrderSchema):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT price FROM food_items WHERE item_id = %s", (order.item_id,))
        item = cursor.fetchone()
        if not item:
            cursor.close()
            conn.close()
            raise ValueError(f"Food Item ID {order.item_id} does not exist.")

        total_price = OrderCalculatorController.calculate_total(float(item['price']), order.quantity)
        order_time = datetime.now()

        query = "INSERT INTO orders (customer_name, item_id, quantity, total_price, order_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (order.customer_name.strip(), order.item_id, order.quantity, total_price, order_time))
        conn.commit()
        order_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"order_id": order_id, "status": "Order Created", "total_price": total_price}

    def get_all_orders(self):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o.order_id, o.customer_name, o.item_id, o.quantity, 
                   o.total_price, o.order_date, f.name AS item_name
            FROM orders o
            LEFT JOIN food_items f ON o.item_id = f.item_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def update_order(self, order_id: int, updates: UpdateOrderSchema):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        existing = cursor.fetchone()
        if not existing:
            cursor.close()
            conn.close()
            raise ValueError(f"Order ID {order_id} not found.")

        new_c_name = updates.customer_name if updates.customer_name is not None else existing['customer_name']
        new_item_id = updates.item_id if updates.item_id is not None else existing['item_id']
        new_qty = updates.quantity if updates.quantity is not None else existing['quantity']

        cursor.execute("SELECT price FROM food_items WHERE item_id = %s", (new_item_id,))
        item = cursor.fetchone()
        if not item:
            cursor.close()
            conn.close()
            raise ValueError(f"Food Item ID {new_item_id} does not exist.")

        new_total = OrderCalculatorController.calculate_total(float(item['price']), new_qty)

        query = "UPDATE orders SET customer_name = %s, item_id = %s, quantity = %s, total_price = %s WHERE order_id = %s"
        cursor.execute(query, (new_c_name, new_item_id, new_qty, new_total, order_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Order {order_id} updated successfully."}

    def delete_order(self, order_id: int):
        conn = self.db_controller.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            raise ValueError(f"Order ID {order_id} not found.")
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Order {order_id} deleted successfully."}