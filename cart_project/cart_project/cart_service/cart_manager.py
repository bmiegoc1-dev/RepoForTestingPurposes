from infrastructure.models import db, Product, CartItem, Users
from exceptions.exceptions import UserNotFoundError, ProductNotFoundError


class CartManager:

    def add_to_cart(self, item: CartItem) -> str:
        product = db.session.get(Product, item.product_id)
        if not product:
            raise ProductNotFoundError(f"Product {item.product_id} does not exist")

        existing_item = db.session.execute(
            db.select(CartItem).filter_by(user_id=item.user_id, product_id=item.product_id)
        ).scalar_one_or_none()

        if existing_item:
            existing_item.quantity += item.quantity
        else:
            db.session.add(item)
        db.session.commit()

        return product.name

    def remove_from_cart(self, item: CartItem) -> str:
        existing_item = db.session.execute(
            db.select(CartItem).filter_by(user_id=item.user_id, product_id=item.product_id)
        ).scalar_one_or_none()
        if not existing_item:
            raise ProductNotFoundError(f"Product {item.product_id} not in cart for user {item.user_id}")

        existing_item.quantity -= item.quantity
        if existing_item.quantity <= 0:
            db.session.delete(existing_item)

        db.session.commit()

        product_name = db.session.get(Product, item.product_id)

        return product_name.name

    def get_total(self, user_id: int) -> float:
        existing_user = db.session.get(Users, user_id)

        if existing_user is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        items_of_user = db.session.execute(
            db.select(CartItem).filter_by(user_id=user_id)
        ).scalars().all()

        total = 0
        for item in items_of_user:
            product_price = db.session.get(Product, item.product_id)
            total += item.quantity * product_price.price

        return float(total)

    def get_cart(self, user_id: int) -> dict:
        user_object = db.session.get(Users, user_id)

        if user_object is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        items_of_user = db.session.execute(
            db.select(CartItem).filter_by(user_id=user_id)
        ).scalars().all()

        username = user_object.username

        if not items_of_user:
            return {"cart_owner": username, "items": [], "total_value": 0}

        formatted_cart = [i.to_dict() for i in items_of_user]

        cart_total = 0
        for item in formatted_cart:
            cart_total += item["total"]

        return {
            "cart_owner": username,
            "items": formatted_cart,
            "total_value": cart_total
        }
