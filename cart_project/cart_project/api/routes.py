from flask import Blueprint, request, jsonify, Response
from cart_service.cart import CartManager, StoreManager
from infrastructure.models import db, Product, CartItem

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
            "error": "bad request",
            "message" : "invalid data type. Parameters must be numbers."
        }), 400



    my_cart_manager = CartManager()

    #Calling the right method to perform an action.
    product_to_add = my_cart_manager.add_to_cart(new_cart_item)

    if product_to_add == "Not found":
        return jsonify({
            "error" : "data not found",
            "possible_reasons" : "product ID does not exist"
        }), 404

    # 4. Send back the response to the user
    return jsonify({"message": f"Successfully added {product_to_add} x{new_cart_item.quantity} times to your cart!"}), 201



@cart_bp.route('/remove', methods=['DELETE'])

def api_remove_from_cart() -> tuple[Response, int]:           ### Removes item from the cart

    data = request.get_json()

    try:
        item_to_remove = CartItem.from_dict(data)  # ## Adding the method to clean incoming data. Variable holds the
                                                    # data entered by the user
    except ValueError:
        return jsonify({
            "error" : "bad request",
            "message": "invalid data type, parameters must be numbers."
        }), 400

    my_cart_manager = CartManager()

    # Calling the method to perform an action

    item_removing = my_cart_manager.remove_from_cart(item_to_remove)  # Contains return statement

    if item_removing == "Not found":  # handling the not found error
        return jsonify({
            "error": "data not found",
            "possible_reasons": "product id does not exist"
        }), 404

    # 4. Send back the response to the user
    return jsonify({"message": f"Successfully removed x{item_to_remove.quantity}  {item_removing}! "}), 200







@cart_bp.route('/total/<int:user_id>', methods=['GET'])
def api_get_total(user_id : int) -> tuple[Response, int]:       #### Total cart value
    my_cart_manager = CartManager()

    try:
        current_price = my_cart_manager.get_total(user_id)
    except ValueError:
        return jsonify({
            "error": "data not found",
            "possible_reasons": "user id does not exist"
        }), 404


    return jsonify({"current_cart_value": current_price}), 200


@cart_bp.route('/add_store', methods=['POST'])    # Adding an item to the catalog
def api_store_item() -> tuple[Response, int]:
    data = request.get_json()

    try:
        new_store_item = Product.from_dict(data)    # using the from_dict method to clean incoming data
    except ValueError:  # In case of invalid data entered while trying to add an item, produce ValueError
        return jsonify({
            "error": "bad request",
            "possible_reasons": "invalid data type"
        }), 400

    my_store_manager = StoreManager()

    item_to_add = my_store_manager.add_to_store(new_store_item)


    return jsonify({"message": f"Successfully added {item_to_add} x {new_store_item.quantity} times to the catalog"}), 201






@cart_bp.route('/catalog', methods=['GET'])
def api_get_catalog() -> tuple[Response,int]:

    my_store_manager = StoreManager()

    current_catalog = my_store_manager.get_catalog()

    return jsonify({"catalog": current_catalog}), 200






@cart_bp.route('/get_cart/<int:user_id>', methods=['GET'])
def api_get_cart(user_id : int)  -> tuple[Response, int]:

    my_cart_manager = CartManager()

    user_cart = my_cart_manager.get_cart(user_id)

    if "not_found" in user_cart:  # Extracting the error mesage from get_cart method.
        return jsonify(user_cart), 404


    return jsonify(user_cart), 200














