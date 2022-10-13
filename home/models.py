import typing as t
from pydantic import BaseModel

class CartProductModelIn(BaseModel):
    productId: int

class CartProductModelOut(BaseModel):
    cartUuid: t.Any
    productName: str