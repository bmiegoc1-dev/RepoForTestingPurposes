from infrastructure.models import db, Product, CartItem, Users


class CartManager:

    def add_to_cart(self, item : CartItem)  -> str:  # Passing the CartItem object (created with from_dict method) as
        # the parameter

        # Looking for a product name, if the user is trying to add the product that doesn't exist in the inventory,
        # it will throw a response.
        product_name = db.session.get(Product, item.product_id)
        if not product_name:
            return "Not found"

        #Searching for existing item in database
        existing_item = CartItem.query.filter_by(user_id=item.user_id, product_id=item.product_id).first()
        if existing_item: # if true - increase quantity
            existing_item.quantity += item.quantity
        else: # else - create a new row with item
            db.session.add(item)
        # Save changes
        db.session.commit()

        return product_name.name  # functions return the product name.



    def remove_from_cart(self, item: CartItem) -> str:
        # Looks for existing item in database
        existing_item = CartItem.query.filter_by(user_id=item.user_id, product_id=item.product_id).first()
        if not existing_item:
            return "Not found"

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
            raise ValueError("The user_id does not exist")

        items_of_user = CartItem.query.filter_by(user_id=user_id).all()   #filtering for all results of given user_id

        total = 0  # counter
        for item in items_of_user:   # Iterates through the filtered user items
            product_price = db.session.get(Product, item.product_id)   # Grabs the price of product
            total += item.quantity * product_price.price  # Calculating the total and adding it to the counter

        return total

    def get_cart(self, user_id: int) -> dict:

        user_object = db.session.get(Users, user_id)

        if user_object is None:  # Checks if user does exist
            return {"not_found": "User does not exist"}

        items_of_user = CartItem.query.filter_by(user_id=user_id).all()



        if not items_of_user:   # If it's true and the code comes to this point, the user's cart must be empty
            return {
                "not_found": "This user's cart is empty"
            }

        username = user_object.username # Grabs the username for better layout at the end.


        formatted_cart = [  # Formatting cart to dictionary.
            i.to_dict() for i in items_of_user
        ]

        cart_total = 0

        for item in formatted_cart:
            cart_total += item["total"] #Looks for a total for each item in our formatted cart and adds this value to our cart_total which is a full cart total value

        return {
            "cart_owner": username,
            "items": formatted_cart,  # Formatted list of dictionaries
            "total_value": cart_total
        }




class StoreManager:  # Class responsible for Store managing.

    def add_to_store(self, item: Product) -> str:  # I passed the fully built Product object, that has been created with from_dict method.

        existing_item = Product.query.filter_by(name=item.name).first()   #Checking if the product we are trying to add already exists
        if existing_item:  # if it is - increase  a quantity
            existing_item.quantity += item.quantity
        else:
            db.session.add(item) # Adding the item to the product table

        db.session.commit()

        return item.name  # method returns the item name.



    def get_catalog(self) -> list[dict]:

        whole_catalog = Product.query.all()

        formatted_catalog = [
            i.to_dict() for i in whole_catalog
        ]




        return formatted_catalog























