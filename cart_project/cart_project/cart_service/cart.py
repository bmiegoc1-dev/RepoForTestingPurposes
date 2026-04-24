from infrastracture.models import db, Product, CartItem

class ShoppingCart:
    def __init__(self):
        # Stores items as {item_name: {"price": float, "quantity": int}}
        self.items = {}

    def add_item(self, name :str, price :int, quantity=1):           #### cola. 10$, 3
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name, quantity=1):
        if name in self.items:
            self.items[name]["quantity"] -= quantity
            if self.items[name]["quantity"] <= 0:
                del self.items[name]

    def get_total(self) -> int:
        total = 0
        for item in self.items.values():
            total += item["price"] * item["quantity"]
        return total


my_cart = ShoppingCart()



# Class to look for duplicated object inside cart to prevent from creating new rows


class CartManager:

    def add_to_cart(self, item : CartItem)  -> str:  # Passing the CartItem object (created with from_dict method) as the parameter
        #Searching for existing item in database
        existing_item = CartItem.query.filter_by(user_id=item.user_id, product_id=item.product_id).first()
        if existing_item: # if true - increase quantity
            existing_item.quantity += item.quantity
        else: # else - create a new row with item
            db.session.add(item)
        # Save changes
        db.session.commit()
        # Looking for a product name for handling response  and sending it back to the route.
        product_name = Product.query.get(item.product_id)
        return product_name.name  # functions return the product name.











