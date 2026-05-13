from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey
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



    REQUIRED_FIELDS = {"user_id", "product_id", "quantity"}   # Specifying fields that are required to pass to handle missing fields error

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CartItem':
        clean_data = data.copy()

        missing = cls.REQUIRED_FIELDS - clean_data.keys()  # Compares fields typed by the user with required.
        if missing:  # If condition is true (any fields remained after subtraction) raise ValueError
            raise ValueError(f"Missing required fields: {missing}")
        if clean_data.get("user_id"):
            clean_data["user_id"] = int(clean_data["user_id"])

        if clean_data.get("product_id"):
            clean_data["product_id"] = int(clean_data["product_id"])

        if clean_data.get("quantity"):
            clean_data["quantity"] = int(clean_data["quantity"])

        return cls(**{k : v for k,v in clean_data.items() if k in cls.__annotations__})

    def to_dict(self) -> dict:  # Method that creates a dictionary with desired data to display for the user

        cart_dictionary = {   # What I need here is username, name of the product, quantity, and total value of the product
            "product_name" : self.product.name,
            "price": float(self.product.price),
            "quantity" : self.quantity,
            "total": float(self.product.price * self.quantity)

        }

        return cart_dictionary



class Product(db.Model):

    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)

    quantity: Mapped[int] = mapped_column(nullable=False)

    REQUIRED_FIELDS = {"name", "price", "quantity"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Product':

        clean_data = data.copy()

        missing = cls.REQUIRED_FIELDS - clean_data.keys()
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        if clean_data.get("name"):
            clean_data["name"] = str(clean_data["name"])
        if clean_data.get("price") is not None:
            clean_data["price"] = Decimal(str(clean_data["price"]))
        if clean_data.get("quantity"):
            clean_data["quantity"] = int(clean_data["quantity"])

        return cls(**{k : v for k,v in clean_data.items() if k in cls.__annotations__})



    def to_dict(self) -> dict:

        product_dictionary = {
            "name": self.name,
            "price": float(self.price),
            "quantity": self.quantity
        }

        return product_dictionary





















