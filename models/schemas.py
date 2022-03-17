from typing import Optional

from pydantic import BaseModel


class ProductURLAndIDCreate(BaseModel):
    url: str


class ProductURLAndID(ProductURLAndIDCreate):
    id: int

    class Config:
        orm_mode = True


class ProductsInfoCreate(BaseModel):
    name: str
    full_price: int
    price_with_card: int
    price_on_sale: int


class ProductInfo(ProductsInfoCreate):
    product_id: int

    class Config:
        orm_mode = True
