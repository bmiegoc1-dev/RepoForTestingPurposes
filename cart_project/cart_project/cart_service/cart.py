from infrastructure.models import db, Product, CartItem, Users
from exceptions.exceptions import UserNotFoundError, ProductNotFoundError


class CartManager:

    def add_to_cart(self, item : CartItem)  -> str:  # Passing the CartItem object (created with from_dict method) as
        # the parameter

        # Looking for a product name, if the user is trying to add the product that doesn't exist in the inventory,
        # it will throw an error
        product = db.session.get(Product, item.product_id)
        if not product:
            raise ProductNotFoundError(f"Product{item.product_id} does not exist")

        #Searching for existing item in database
        existing_item = db.session.execute(
            db.select(CartItem).filter_by(user_id=item.user_id, product_id=item.product_id)
        ).scalar_one_or_none()

        if existing_item: # if true - increase quantity
            existing_item.quantity += item.quantity
        else: # else - create a new row with item
            db.session.add(item)
        # Save changes
        db.session.commit()

        return product.name



    def remove_from_cart(self, item: CartItem) -> str:
        # Looks for existing item in database
        existing_item = db.session.execute(
            db.select(CartItem).filter_by(user_id=item.user_id, product_id=item.product_id)
        ).scalar_one_or_none()
        if not existing_item:
            raise ProductNotFoundError(f"Product {item.product_id} not in cart for user {item.user_id}")

        existing_item.quantity -= item.quantity
        if existing_item.quantity <= 0:  # after subtracting quantity, if it goes down to zero, remove whole item
            # from the cart
            db.session.delete(existing_item)

        db.session.commit()

        # # Looking for a product name for handling response  and sending it back to the route.
        product_name = db.session.get(Product, item.product_id)

        return product_name.name  # Function returns product name


    def get_total(self, user_id: int) -> float:


        existing_user = db.session.get(Users, user_id) # Checking if the entered user_id exist

        if existing_user is None: # If it doesn't - raise valueError
            raise UserNotFoundError(f"User {user_id} does not exist")

        items_of_user = db.session.execute(  #filtering for all results of given user_id
            db.select(CartItem).filter_by(user_id=user_id)
        ).scalars().all()

        total = 0# counter
        for item in items_of_user:   # Iterates through the filtered user items
            product_price = db.session.get(Product, item.product_id)   # Grabs the price of product
            total += item.quantity * product_price.price  # Calculating the total and adding it to the counter

        return float(total)

    def get_cart(self, user_id: int) -> dict:

        user_object = db.session.get(Users, user_id)

        if user_object is None:  # Checks if user does exist
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




class StoreManager:  # Class responsible for Store managing.

    def add_to_store(self, item: Product) -> str:  # I passed the fully built Product object, that has been created with from_dict method.

        existing_item = db.session.execute(          #Checking if the product we are trying to add already exists
            db.select(Product).filter_by(name=item.name)
        ).scalar_one_or_none()

        if existing_item:  # if it is - increase  a quantity
            existing_item.quantity += item.quantity
        else:
            db.session.add(item) # Adding the item to the product table

        db.session.commit()

        return item.name  # method returns the item name.



    def get_catalog(self) -> list[dict]:

        whole_catalog = db.session.execute(db.select(Product)).scalars().all()


        formatted_catalog = [
            i.to_dict() for i in whole_catalog
        ]




        return formatted_catalog























