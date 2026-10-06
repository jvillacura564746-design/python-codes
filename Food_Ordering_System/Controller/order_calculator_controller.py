class OrderCalculatorController:
    @staticmethod
    def calculate_total(price: float, quantity: int) -> float:
        return round(price * quantity, 2)