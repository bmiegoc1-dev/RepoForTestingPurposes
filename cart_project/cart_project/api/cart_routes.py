from flask import Blueprint, request, jsonify, Response
from cart_service.cart_manager import CartManager
from infrastructure.models import CartItem
from exceptions.exceptions import UserNotFoundError, ProductNotFoundError


cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/add', methods=['POST'])
def api_add_to_cart() -> tuple[Response, int]:
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        new_cart_item = CartItem.from_dict(data)
    except ValueError:
        return jsonify({"error": "Invalid data types"}), 400

    my_cart_manager = CartManager()

    try:
        product_to_add = my_cart_manager.add_to_cart(new_cart_item)
    except ProductNotFoundError:
        return jsonify({"error": "Product does not exist"}), 404

    return jsonify({"message": f"Successfully added {product_to_add} x{new_cart_item.quantity} times to your cart!"}), 201


@cart_bp.route('/remove', methods=['DELETE'])
def api_remove_from_cart() -> tuple[Response, int]:
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        item_to_remove = CartItem.from_dict(data)
    except ValueError:
        return jsonify({"error": "invalid data types"}), 400

    my_cart_manager = CartManager()

    try:
        item_removing = my_cart_manager.remove_from_cart(item_to_remove)
    except ProductNotFoundError:
        return jsonify({"error": "Product not found in cart"}), 404

    return jsonify({"message": f"Successfully removed x{item_to_remove.quantity} {item_removing}!"}), 200


@cart_bp.route('/total/<int:user_id>', methods=['GET'])
def api_get_total(user_id: int) -> tuple[Response, int]:
    my_cart_manager = CartManager()

    try:
        current_price = my_cart_manager.get_total(user_id)
    except UserNotFoundError:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify({"current_cart_value": current_price}), 200


@cart_bp.route('/get_cart/<int:user_id>', methods=['GET'])
def api_get_cart(user_id: int) -> tuple[Response, int]:
    my_cart_manager = CartManager()

    try:
        user_cart = my_cart_manager.get_cart(user_id)
    except UserNotFoundError:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify(user_cart), 200
