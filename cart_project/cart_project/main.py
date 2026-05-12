from flask import Flask
from infrastructure.models import db  # imported  db classes and db toolkit
from api.routes import cart_bp
import os
from dotenv import load_dotenv



# Creating the app
app = Flask(__name__)

#Loading environmental  variables to the file
load_dotenv()
# Providing a db connection address for our app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# Starting the SQLAlchemy manager - initialize the database from another file
db.init_app(app)

#Initializing the endpoints from routes with blueprint
app.register_blueprint(cart_bp)


# Server setup
if __name__ == '__main__':
    app.run(debug=True)