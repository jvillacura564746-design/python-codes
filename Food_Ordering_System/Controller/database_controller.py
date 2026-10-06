import mysql.connector


class DatabaseController:
    def __init__(self, host="localhost", user="root", password="", database="food_ordering_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.use_mysql = True

        # Fallback storage if MySQL server is down
        self.food_items = [
            {"id": 1, "name": "Cheeseburger", "category": "Burger", "price": 150.0},
            {"id": 2, "name": "Pepperoni Pizza", "category": "Pizza", "price": 350.0},
            {"id": 3, "name": "Chicken Wings", "category": "Chicken", "price": 280.0},
        ]
        self.orders = []

        try:
            self._initialize_database()
        except mysql.connector.Error as err:
            print(f"[WARNING]: Could not connect to MySQL server ({err}). Switching to in-memory mode.")
            self.use_mysql = False


    def get_connection(self):
        """Returns a active MySQL database connection."""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def _initialize_database(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        conn.close()

    def get_all_orders(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        # JOIN orders and food_items so item_name is always included
        query = """
            SELECT o.order_id, o.customer_name, o.item_id, o.quantity, o.total_price, f.name AS item_name 
            FROM orders o 
            LEFT JOIN food_items f ON o.item_id = f.id
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        conn.close()
        return orders