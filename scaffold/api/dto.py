from datetime import datetime
from typing import List

from api.models import Item, Order
from ninja import Field, ModelSchema, Schema


class ErrResponse(Schema):
    msg: str


class ValidateErrResponse(Schema):
    detail: List[dict]


class ItemRequest(Schema):
    name: str = Field(..., max_length=255)
    stock: int = Field(0, gt=0)
    sold: int = Field(0, ge=0)
    last: datetime = Field(datetime.now())


class ItemResponse(ModelSchema):
    class Config:
        model = Item
        model_fields = ["id", "create_time", "update_time", "name", "stock", "sold", "last"]


class OrderRequest(Schema):
    id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    buy: int = Field(..., gt=0)


class OrderResponse(ModelSchema):
    item: ItemResponse

    class Config:
        model = Order
        model_fields = ["id", "create_time", "update_time", "quantity"]
