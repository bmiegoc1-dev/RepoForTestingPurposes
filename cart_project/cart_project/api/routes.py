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
            "Error": "Bad request",
            "Message" : "Invalid data type. Parameters must be numbers."
        }), 400



    my_cart_manager = CartManager()  # Class instance object

    #Calling the right method to perform an action.
    product_to_add = my_cart_manager.add_to_cart(new_cart_item)

    if product_to_add == "Not found":
        return jsonify({
            "Error" : "Data not found",
            "Possible reasons" : "Product ID does not exist"
        }), 404

    # 4. Send back the response to the user
    return jsonify({"message": f"Succesfully added {product_to_add} x{new_cart_item.quantity} times to your cart!"}), 201



@cart_bp.route('/remove', methods=['DELETE'])

def api_remove_from_cart() -> tuple[Response, int]:           ### Removes item from the cart

    data = request.get_json()

    try:
        item_to_remove = CartItem.from_dict(data)  # ## Adding the method to clean incoming data. Variable holds the
                                                    # data entered by the user
    except ValueError:
        return jsonify({
            "error" : "bad request",
            "message": "Invalid data type. Parameters must be numbers."
        }), 400

    my_cart_manager = CartManager()  # Class instance object

    # Calling the method to perform an action

    item_removing = my_cart_manager.remove_from_cart(item_to_remove)  # Contains return statement

    if item_removing == "Not found":  # handling the not found error
        return jsonify({
            "error": "data not found",
            "possible_reasons": "product id does not exist"
        }), 404

    # 4. Send back the response to the user
    return jsonify({"message": f"Succesfully removed x{item_to_remove.quantity}  {item_removing}! "}), 200







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


