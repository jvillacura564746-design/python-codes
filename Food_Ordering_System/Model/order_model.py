from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class OrderModel:
    order_id: Optional[int]
    customer_name: str
    item_id: int
    quantity: int
    total_price: float
    order_date: Optional[datetime] = None