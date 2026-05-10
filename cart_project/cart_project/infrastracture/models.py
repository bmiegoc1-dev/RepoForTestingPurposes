from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, ForeignKey, DateTime
from typing import Any


db = SQLAlchemy()



class Users(db.Model):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    password: Mapped[str] = mapped_column(String(50), nullable=False)


    


class CartItem(db.Model):

    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)

    quantity: Mapped[int] = mapped_column(nullable=False)

    product = db.relationship('Product')




    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CartItem':
        clean_data = data.copy()
        if clean_data.get("user_id"):  # using get here prevents from crashing when user won't send this data. KeyError
            clean_data["user_id"] = int(clean_data["user_id"])

        if clean_data.get("product_id"):
            clean_data["product_id"] = int(clean_data["product_id"])

        if clean_data.get("quantity"):
            clean_data["quantity"] = int(clean_data["quantity"])

        return cls(**{k : v for k,v in clean_data.items() if k in cls.__annotations__})

    def to_dict(self) -> dict:  # Method that creates a dictionary with desired data to display for the user

        cart_dictionary = {   # What I need here is username, name of the product, quantity, and total value of the product
            "product_name" : self.product.name,
            "price": self.product.price,
            "quantity" : self.quantity,
            "total": self.product.price * self.quantity

        }

        return cart_dictionary



class Product(db.Model):

    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)

    quantity: Mapped[int] = mapped_column(nullable=False)



    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Product':

        clean_data = data.copy()

        if clean_data.get("name"):
            clean_data["name"] = str(clean_data["name"])
        if clean_data.get("price"):
            clean_data["price"] = int(clean_data["price"])
        if clean_data.get("quantity"):
            clean_data["quantity"] = int(clean_data["quantity"])

        return cls(**{k : v for k,v in clean_data.items() if k in cls.__annotations__})



    def to_dict(self) -> dict:

        product_dictionary = {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }

        return product_dictionary





















