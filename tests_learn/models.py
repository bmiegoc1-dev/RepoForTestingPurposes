from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Users(db.Model):
    # 1. The primary Key column, ID.
    id = db.Column(db.Integer, nullable=False, primary_key=True)

    # 2. Username column
    username = db.Column(db.String(80), nullable=False, unique=True)

    # 3. Password column
    password = db.Column(db.String(50), nullable=False)


class CartItem(db.Model):
    # 1 id column
    id = db.Column(db.Integer,
                   primary_key=True)  # there's no need to write nullable=false. When there is primary key, sql use nullable=false by default
    # 2 quantity column
    quantity = db.Column(db.Integer, nullable=False)
    # 3 product_id column
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    # 4 user_id column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Product(db.Model):
    # 1. id column
    id = db.Column(db.Integer, primary_key=True)
    # 2. name column
    name = db.Column(db.String(50), nullable=False)
    # 3. price column
    price = db.Column(db.Numeric(10, 2), nullable=False)
    # 4. quantity column
    quantity = db.Column(db.Integer, nullable=False)