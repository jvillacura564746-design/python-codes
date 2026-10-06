from dataclasses import dataclass

@dataclass
class ReportModel:
    total_revenue: float
    average_order_value: float
    std_order_value: float
    first_order_date: str
    latest_order_date: str