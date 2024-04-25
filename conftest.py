import pytest
import sqlite3

from app import create_app, db
from app.models import Cart, Order, Product, User


@pytest.fixture(scope='session')
def test_app():
    """Create a test Flask app."""
    app = create_app('app.config.TestingConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def session():
    connection = sqlite3.connect(':memory:')
    test_app = create_app('app.config.TestingConfig')
    test_app.app_context().push()
    db.app = test_app
    db.create_all()

    yield db.session

    connection.close()


@pytest.fixture(scope='function')
def user(session):
    user = User(name="test_name", email="test_email", address="test_address")
    session.add(user)
    session.commit()
    return user


@pytest.fixture(scope='function')
def admin(session):
    admin = User(name="admin", email="admin_email", address="admin_address",
                 is_admin=True)
    session.add(admin)
    session.commit()
    return admin


@pytest.fixture(scope='function')
def cart(user, session):
    cart = Cart(user=user)
    session.add(cart)
    session.commit()
    return cart

@pytest.fixture(scope='function')
def product(session):
    product = Product(name="test_product", description="test_description",
                      price=5.99, stock=100)
    session.add(product)
    session.commit()
    return product


@pytest.fixture(scope='function')
def products(session):
    product_1 = Product(name="test_product_1", description="test_description_1",
                        price=5.99, stock=100)
    product_2 = Product(name="test_product_2", description="test_description_2",
                        price=10.99, stock=100)
    session.add_all([product_1, product_2])
    session.commit()
    return product_1, product_2


@pytest.fixture(scope='function')
def cart_item(session, cart, product):
    cart.add_product(product.id)
    session.commit()
    return cart.items[0]

@pytest.fixture(scope='function')
def order(session, user, cart, products):
    for product in products:
        cart.add_product(product.id)
    order = Order.create_order_from_cart(cart)
    session.add(order)
    session.commit()
    return order

@pytest.fixture(scope='function')
def order_item(session, order):
    return order.items[0]
