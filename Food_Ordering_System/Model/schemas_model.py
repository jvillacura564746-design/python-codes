from pydantic import BaseModel, Field
from typing import Optional

class FoodItemSchema(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

class UpdateFoodItemSchema(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class OrderSchema(BaseModel):
    customer_name: str = Field(..., min_length=1)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class UpdateOrderSchema(BaseModel):
    customer_name: Optional[str] = None
    item_id: Optional[int] = None
    quantity: Optional[int] = None