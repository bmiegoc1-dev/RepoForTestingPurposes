from flask import Blueprint, request, jsonify, Response
from cart_service.store_manager import StoreManager
from infrastructure.models import Product


store_bp = Blueprint('store', __name__)


@store_bp.route('/add_store', methods=['POST'])
def api_store_item() -> tuple[Response, int]:
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    try:
        new_store_item = Product.from_dict(data)
    except ValueError:
        return jsonify({
            "error": "bad request",
            "possible_reasons": "invalid data type"
        }), 400

    my_store_manager = StoreManager()
    item_to_add = my_store_manager.add_to_store(new_store_item)

    return jsonify({"message": f"Successfully added {item_to_add} x {new_store_item.quantity} times to the catalog"}), 201


@store_bp.route('/catalog', methods=['GET'])
def api_get_catalog() -> tuple[Response, int]:
    my_store_manager = StoreManager()
    current_catalog = my_store_manager.get_catalog()

    return jsonify({"catalog": current_catalog}), 200
