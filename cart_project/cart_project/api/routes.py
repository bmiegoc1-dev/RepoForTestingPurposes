from flask import Blueprint, request, jsonify, Response
from cart_service.cart import CartManager, StoreManager
from infrastructure.models import db, Product, CartItem
from exceptions.exceptions import UserNotFoundError, ProductNotFoundError


cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def api_add_to_cart() ->tuple[Response, int]:  # adding item to the cart_item table

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        new_cart_item = CartItem.from_dict(data)
    except ValueError:  # If any data is not required type and it produces ValueError, return this response to the user.
        return jsonify({
            "error": "Invalid data types"}), 400



    my_cart_manager = CartManager()

    try:
        # Calling the right method to perform an action.
        product_to_add = my_cart_manager.add_to_cart(new_cart_item)

    except ProductNotFoundError:
        return jsonify({"error": "Product does not exist"}), 404

    # 4. Send back the response to the user
    return jsonify({"message": f"Successfully added {product_to_add} x{new_cart_item.quantity} times to your cart!"}), 201



@cart_bp.route('/remove', methods=['DELETE'])

def api_remove_from_cart() -> tuple[Response, int]:  # Removes item from the cart

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        item_to_remove = CartItem.from_dict(data)
    except ValueError:
        return jsonify({"error": "invalid data types"}), 400

    my_cart_manager = CartManager()

    # Calling the method to perform an action

    try:
        item_removing = my_cart_manager.remove_from_cart(item_to_remove)  # Contains return statement

    except ProductNotFoundError:
        return jsonify({"error": "Product not found in cart"}), 404

    # 4. Send back the response to the user
    return jsonify({"message": f"Successfully removed x{item_to_remove.quantity} {item_removing}!"}), 200







@cart_bp.route('/total/<int:user_id>', methods=['GET'])
def api_get_total(user_id : int) -> tuple[Response, int]:       #### Total cart value
    my_cart_manager = CartManager()

    try:
        current_price = my_cart_manager.get_total(user_id)
    except UserNotFoundError:
        return jsonify({"error": "User does not exist"}), 404



    return jsonify({"current_cart_value": current_price}), 200


@cart_bp.route('/add_store', methods=['POST'])    # Adding an item to the catalog
def api_store_item() -> tuple[Response, int]:
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        new_store_item = Product.from_dict(data)
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

    try:
        user_cart = my_cart_manager.get_cart(user_id)
    except UserNotFoundError:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify(user_cart), 200














