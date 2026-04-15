from flask import Blueprint, request, jsonify
from cart import my_cart
from infrastracture.models import db, Product, CartItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def api_add_item():        ### adding item to the cart table

    #1. Catch the incoming data, entered by user and save it to the variable.
    data = request.get_json()
    # 2. Extract values from dictionary for easier managing.
    user_id= int(data.get("user_id"))
    product_id = int(data.get("product_id"))   # pass it to the variable
    item_quantity = int(data.get("quantity"))

    # Maps the data to our table
    cart_item_info = CartItem(user_id=user_id, product_id=product_id, quantity=item_quantity)

    #Saves the output to the database
    db.session.add(cart_item_info)
    db.session.commit()

    name_of_product = Product.query.get(product_id)
    name_dict ={
        "name" : name_of_product.name
    }

    # 4. Send back the response to they user. We use jsonify for the machine to understand the language
    return jsonify({"message": f"Succesfully added {name_dict['name']} x{item_quantity} times to your cart!"}), 201



@cart_bp.route('/remove', methods=['DELETE'])

def api_remove_item():           ### Removes item from the cart

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
def api_get_total():          #### Total cart value
    current_price = my_cart.get_total()
    return jsonify({"Current cart value is:": current_price})


@cart_bp.route('/store', methods=['POST'])    # Adding an item to the catalog
def api_store_item():
    data = request.get_json()
    item_name = data.get("name")
    item_price = data.get("price")
    item_quantity = data.get("quantity")
    product_info = Product(name=item_name, price=item_price, quantity=item_quantity)
    db.session.add(product_info)
    db.session.commit()

    # Is it necessary here?  all_products= Product.query.all()

    return jsonify({"message:": f"Successfully added {item_name} x{item_quantity} to the catalog"}), 201


@cart_bp.route('/catalog', methods=['GET'])
def api_get_catalog():
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
def api_get_id_product(id):

    single_product = Product.query.get(id)   # Queries for only one product
    id_product = single_product.id

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


