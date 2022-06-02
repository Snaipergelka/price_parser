from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class ProductsIDAndURL(Base):
    __tablename__ = "products_id_and_url"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    url = Column(String, index=True, unique=True)


class ProductsInfo(Base):
    __tablename__ = "products_information"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, index=True, unique=True)
    full_price = Column(Integer)
    price_with_card = Column(Integer)
    price_on_sale = Column(Integer)
    product_id = Column(Integer, ForeignKey("products_id_and_url.id"))


class User(Base):
    __tablename__ = "users_authorization_information"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    phone_number = Column(String, index=True, unique=True)


class UserAndProductID(Base):
    __tablename__ = "users_and_product_id"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    product_id = Column(Integer, ForeignKey("products_information.id"))
    user_id = Column(Integer, ForeignKey("users_authorization_information.id"))
