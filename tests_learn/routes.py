from flask import Blueprint, request, jsonify
from cart import ShoppingCart, my_cart


cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def api_add_item():

    #1. Catch the incoming data, entered by user and save it to the variable.
    data = request.get_json()
    # 2. Extract values from dictionary for easier managing.
    item_name = data.get("name")
    item_price = data.get("price")
    item_quantity = data.get("quantity")

    # 3. Feed them into our existing class method.

    my_cart.add_item(item_name,item_price, item_quantity)

    # 4. Send back the response to they user. We use jsonify for the machine to understand the language
    return jsonify({"message": f"Succesfully added {item_name}!"}), 201



@cart_bp.route('/remove', methods=['DELETE'])

def api_remove_item():

    # 1. Catching the data
    data = request.get_json()
    # 2. Extracting the desired values
    item_name = data.get("name")
    item_quantity = data.get("quantity")
    # 3. Triggering the method
    my_cart.remove_item(item_name, item_quantity)
    # 4. Send back the response to the user
    return jsonify({"message": f"Succesfully removed {item_quantity} pieces of {item_name}! "})







@cart_bp.route('/total', methods=['GET'])
def api_get_total():
    current_price = my_cart.get_total()
    return jsonify({"Current cart value is:": current_price})