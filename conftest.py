import pytest
import sqlite3

from app import create_app
from app.extensions import db
from app.models import Cart, Order, Product, User


@pytest.fixture(scope='function')
def test_app():
    """Create a test Flask app."""
    app = create_app('app.config.TestingConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def session():
    """Create a temporary database and app context."""
    connection = sqlite3.connect(':memory:')
    app = create_app('app.config.TestingConfig')
    context = app.app_context()
    context.push()
    db.app = app
    db.create_all()

    yield db.session
    db.drop_all()
    connection.close()
    context.pop()


@pytest.fixture(scope='function')
def client(test_app):
    with test_app.app_context():
        yield test_app.test_client()


@pytest.fixture(scope='function')
def user(session):
    """Add a simple test user to the database."""
    user = User(username="test_username", name="test_name", email="test_email",
                address="test_address")
    user.set_password("correct_password")
    session.add(user)
    session.commit()
    return user


@pytest.fixture(scope='function')
def admin(session):
    """Add an admin test user to the database."""
    admin = User(username="test_admin_username", name="admin",
                 email="admin_email", address="admin_address",
                 is_admin=True)
    admin.set_password("password")
    session.add(admin)
    session.commit()
    return admin


@pytest.fixture(scope='function')
def cart(user, session):
    """Add a cart for the user to the database."""
    cart = Cart(user=user)
    session.add(cart)
    session.commit()
    return cart

@pytest.fixture(scope='function')
def product(session):
    """Add a product to the database."""
    product = Product(name="test_product", description="test_description",
                      price=5.99, stock=100)
    session.add(product)
    session.commit()
    return product


@pytest.fixture(scope='function')
def products(session):
    """Add two products to the database."""
    product_1 = Product(name="test_product_1", description="test_description_1",
                        price=5.99, stock=100)
    product_2 = Product(name="test_product_2", description="test_description_2",
                        price=10.99, stock=100)
    session.add_all([product_1, product_2])
    session.commit()
    return product_1, product_2


@pytest.fixture(scope='function')
def cart_item(session, cart, product):
    """Add a product to the cart."""
    cart.add_product(product.id)
    session.commit()
    return cart.items[0]

@pytest.fixture(scope='function')
def order(session, user, cart, products):
    """Add multiple products to the cart and create an order."""
    for product in products:
        cart.add_product(product.id)
    order = Order.create_order_from_cart(cart)
    session.add(order)
    session.commit()
    return order

@pytest.fixture(scope='function')
def order_item(session, order):
    """Provide a single order item."""
    return order.items[0]
