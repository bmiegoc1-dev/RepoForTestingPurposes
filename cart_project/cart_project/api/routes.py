from click import Tuple
from flask import Blueprint, request, jsonify, Response
from cart_service.cart import my_cart, CartManager
from infrastracture.models import db, Product, CartItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def api_add_to_cart() ->tuple[Response, int]:        ### adding item to the cart_item table

    #1. Catch the incoming data, entered by user and save it to the variable.
    data = request.get_json()

    try:  # Using try to test the code for errors, like value error etc.
        #Using DTO to handle the incoming data Extraction
        new_cart_item = CartItem.from_dict(data)
    except ValueError:  # If any data is not required type and it produces ValueError, return this response to the user.
        return jsonify({
            "Error:": "Bad request",
            "Message:" : "Invalid data type. Parameters must be numbers."
        }), 400



    my_cart_manager = CartManager()  # Class instance object

    #Calling the right method to perform an action.
    product_adding = my_cart_manager.add_to_cart(new_cart_item)

    if product_adding == "Not found":
        return jsonify({
            "Error:" : "Data not found",
            "Possible reasons:" : "Product ID does not exist"
        }), 404

    # 4. Send back the response to they user. We use jsonify for the machine to understand the language
    return jsonify({"message": f"Succesfully added {product_adding} x{new_cart_item.quantity} times to your cart!"}), 201



@cart_bp.route('/remove', methods=['DELETE'])

def api_remove_item() -> tuple[Response, int]:           ### Removes item from the cart

    # 1. Catching the data
    data = request.get_json()
    # 2. Extracting the desired values
    item_name = str(data.get("name"))
    item_quantity = int(data.get("quantity"))
    # 3. Triggering the method
    my_cart.remove_item(item_name, item_quantity)
    # 4. Send back the response to the user
    return jsonify({"message": f"Succesfully removed {item_quantity} pieces of {item_name}! "}), 204







@cart_bp.route('/total', methods=['GET'])
def api_get_total() -> Response:          #### Total cart value
    current_price = int(my_cart.get_total())
    return jsonify({"Current cart value is:": current_price})


@cart_bp.route('/store', methods=['POST'])    # Adding an item to the catalog
def api_store_item() -> tuple[Response, int]:
    data = request.get_json()
    item_name = str(data.get("name"))
    item_price = int(data.get("price"))
    item_quantity = int(data.get("quantity"))
    product_info = Product(name=item_name, price=item_price, quantity=item_quantity)
    db.session.add(product_info)
    db.session.commit()

    # Is it necessary here?  all_products= Product.query.all()

    return jsonify({"message:": f"Successfully added {item_name} x{item_quantity} to the catalog"}), 201


@cart_bp.route('/catalog', methods=['GET'])
def api_get_catalog() -> tuple[Response,int]:
    whole_catalog = Product.query.all()     #querying through our table

    json_ready_catalog = []    # empty dict for translating purposes

    for i in whole_catalog:   # loop iterating through our query

        i_dict = {             # Attaches result to specific data
            "name" : i.name,
            "price" : i.price,
            "quantity" : i.quantity
        }

        json_ready_catalog.append(i_dict)  # Adds sorted results to empty dict

    return  jsonify(json_ready_catalog), 200  # Returns translated dict in json format

@cart_bp.route('/catalog/<int:id>', methods =['GET'])
def api_get_id_product(id) ->tuple[Response, int]:

    single_product = Product.query.get(id)   # Queries for only one product
    id_product = int(single_product.id)

    single_dict = {
        "id": single_product.id,
        "name": single_product.name,
        "price": single_product.price,
        "quantity": single_product.quantity

    }

    return jsonify({"Your product:": single_dict}),200










#TODO recreate another endpoints
#TODO adding http code responses in case of errors
#TODO Dominik's tasks


