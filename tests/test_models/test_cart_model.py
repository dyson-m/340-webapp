import pytest

from app.models import Cart, Product, User


class TestCartModel:
    def test_create_cart(self, session, cart):
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()
        assert fetched_cart.user_id == cart.user.id
        assert cart.user.cart.id == fetched_cart.id

    def test_add_product_to_cart(self, session, cart, product):
        cart.add_product(product.id)
        session.commit()
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()
        assert fetched_cart.items[0].product_id == product.id
        assert fetched_cart.items[0].quantity == 1

    def test_add_product_with_quantity_to_cart(self, session, cart, product):
        cart.add_product(product.id, quantity=3)
        session.commit()
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()
        assert fetched_cart.items[0].product_id == product.id
        assert fetched_cart.items[0].quantity == 3

    def test_remove_product_from_cart_by_product(self, session, cart, product):
        cart.add_product(product.id, quantity=3)
        session.commit()
        assert cart.items[0].product_id == product.id
        cart.remove_product(product.id)
        session.commit()
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()
        assert fetched_cart.items == []

    def test_get_cart_total(self, session, cart, product):
        product_2 = Product(name="test_product_2",
                            description="test_description_2",
                            price=10.99, stock=100)
        session.add(product_2)
        session.commit()
        cart.add_product(product_2.id)
        cart.add_product(product.id, quantity=2)
        cart.add_product(product.id, quantity=3)
        session.commit()
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()

        price = pytest.approx(product.price * 5 + product_2.price * 1)
        assert fetched_cart.get_total_price() == price

    def test_clear_cart(self, session, cart, product):
        cart.add_product(product.id)
        session.commit()
        assert cart.items[0].product_id == product.id
        cart.clear_cart()
        session.commit()
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()
        assert fetched_cart.items == []
