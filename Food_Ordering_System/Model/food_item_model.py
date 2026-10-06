from dataclasses import dataclass
from typing import Optional

@dataclass
class FoodItemModel:
    item_id: Optional[int]
    name: str
    category: str
    price: float