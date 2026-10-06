import uvicorn
from Controller.api_client_controller import ApiClientController
from View.console_view import ConsoleView
from Controller.console_controller import ConsoleController
from Controller.report_controller import ReportController

# api_client = ApiClientController()
# app = api_client.app  # <-- Removed () here
app = ApiClientController()

def run_console_app():
    view = ConsoleView()
    controller = ConsoleController()

    while True:
        view.display_menu()
        choice = view.prompt_choice()

        try:
            if choice == "1":
                c_name, item_id, qty = view.prompt_place_order()
                controller.place_order(c_name, item_id, qty)
                view.display_message("Order placed successfully!")

            elif choice == "2":
                orders = controller.fetch_orders()
                view.display_orders(orders)

            elif choice == "3":
                o_id, c_name, item_id, qty = view.prompt_update_order()
                res = controller.update_order(o_id, c_name, item_id, qty)
                view.display_message(res["message"])

            elif choice == "4":
                o_id = view.prompt_delete_order()
                res = controller.delete_order(o_id)
                view.display_message(res["message"])

            elif choice == "5":
                summary = controller.get_summary()
                view.display_summary(summary)

            elif choice == "6":
                view.display_message("Generating analytics graphs...")
                orders = controller.fetch_orders()
                ReportController.generate_sales_chart(orders)

            elif choice == "0":
                view.display_message("Exiting system...")
                break
            else:
                view.display_error("Invalid choice. Please try again.")

        except Exception as e:
            view.display_error(str(e))

if __name__ == "__main__":
    run_console_app()