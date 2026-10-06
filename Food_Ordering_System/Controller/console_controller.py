from Controller.api_controller import ApiController
from Controller.report_controller import ReportController

class ConsoleController:
    def __init__(self):
        self.api_controller = ApiController()

    def fetch_items(self):
        return self.api_controller.get_all_food_items()

    def add_item(self, name, category, price):
        from Model.schemas_model import FoodItemSchema
        item = FoodItemSchema(name=name, category=category, price=price)
        return self.api_controller.create_food_item(item)

    # Mao ni siya kanang ga read
    def fetch_orders(self):
        return self.api_controller.get_all_orders()

    def place_order(self, customer_name, item_id, quantity):
        from Model.schemas_model import OrderSchema
        order = OrderSchema(customer_name=customer_name, item_id=item_id, quantity=quantity)
        return self.api_controller.create_order(order)

    def update_order(self, order_id, customer_name=None, item_id=None, quantity=None):
        from Model.schemas_model import UpdateOrderSchema
        updates = UpdateOrderSchema(customer_name=customer_name, item_id=item_id, quantity=quantity)
        return self.api_controller.update_order(order_id, updates)

    def delete_order(self, order_id):
        return self.api_controller.delete_order(order_id)

    def get_summary(self):
        orders = self.fetch_orders()
        return ReportController.generate_sales_summary(orders)