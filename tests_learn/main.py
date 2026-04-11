from click import password_option
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db,Users,Product,CartItem   # imported  db classes and db toolkit
from cart import ShoppingCart   # importing the main class service
from enum import unique
from routes import cart_bp


# Creating the app
app = Flask(__name__)
# Providing a db connection address for our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5433/cart_db'

# Starting the SQLAlchemy manager - initialize the databse from another file
db.init_app(app)

#Initializing the endpoints from routes with blueprint
app.register_blueprint(cart_bp)





# testing the functionality and db connection
with app.app_context():
    # Adding the test user to check the connection
   # user1 = Users(username='bartek', password='password1')
    #db.session.add(user1)
    #db.session.commit()


    user2 = Users(username='admin2', password='password2')
    db.session.add(user2)
    db.session.commit()

    # Asks the database for a list of all users
    all_users = Users.query.all()


    print("Connection successful! 🚀 Users found:", all_users)










if __name__ == '__main__':
    app.run(debug=True)