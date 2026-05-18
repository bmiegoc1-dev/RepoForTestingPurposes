from flask import Flask
from infrastructure.models import db
from api.cart_routes import cart_bp
from api.store_routes import store_bp
import os
from dotenv import load_dotenv



#Loading environmental  variables to the file
load_dotenv()

# Creating the app
app = Flask(__name__)

# Providing a db connection address for our app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Starting the SQLAlchemy manager - initialize the database from another file
db.init_app(app)

# Initializing the endpoints from routes with blueprint
app.register_blueprint(cart_bp)
app.register_blueprint(store_bp)


@app.route('/')
def index():
    return app.send_static_file('index.html')


# Server setup
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')