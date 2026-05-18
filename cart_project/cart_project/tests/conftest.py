import pytest
from decimal import Decimal
from flask import Flask
from sqlalchemy.pool import StaticPool

from infrastructure.models import db as _db, Users, Product
from api.cart_routes import cart_bp
from api.store_routes import store_bp


@pytest.fixture
def app():
    test_app = Flask(__name__)
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool,
        },
    })
    _db.init_app(test_app)
    test_app.register_blueprint(cart_bp)
    test_app.register_blueprint(store_bp)

    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seed_data(app):
    user = Users(username='alice', password='password123')
    product = Product(name='Cola', price=Decimal('2.50'), quantity=100)
    _db.session.add_all([user, product])
    _db.session.commit()
    return {'user_id': user.id, 'product_id': product.id}
