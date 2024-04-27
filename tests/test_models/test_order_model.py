import pytest

from app.models import Cart, Order


class TestOrderModel:
    def test_order_creation(self, session, order, products):
        fetched_order = Order.query.first()
        assert fetched_order.user_id == order.user_id
        assert fetched_order.get_total_price() == order.get_total_price()
        assert fetched_order.items[0].product_id == products[0].id
        assert fetched_order.items[1].product_id == products[1].id

    def test_order_creation_from_cart(self, session, cart, products):
        for prod in products:
            cart.add_product(prod.id)
        cart_total = cart.get_total_price()
        new_order = Order.create_order_from_cart(cart)
        session.add(new_order)
        session.commit()
        fetched_order = Order.query.filter(Order.user_id == cart.user.id
                                           ).first()
        assert fetched_order.user_id == cart.user.id
        assert fetched_order.get_total_price() == cart_total

    def test_order_creation_clears_cart(self, session, cart, products):
        for prod in products:
            cart.add_product(prod.id)
        new_order = Order.create_order_from_cart(cart)
        session.add(new_order)
        session.commit()
        fetched_cart = Cart.query.filter(Cart.user_id == cart.user.id).first()
        assert fetched_cart.items == []

    def test_order_creation_updates_stock(self, session, cart, product):
        previous_stock = product.stock
        cart.add_product(product.id, quantity=2)
        new_order = Order.create_order_from_cart(cart)
        session.add(new_order)
        session.commit()
        assert product.stock == previous_stock - 2

    def test_order_creation_fails(self, session, cart, product):
        previous_stock = product.stock
        # ValueError should be raised because there isn't enough stock.
        with pytest.raises(ValueError):
            cart.add_product(product.id, quantity=200)
            new_order = Order.create_order_from_cart(cart)
            session.add(new_order)
            session.commit()
        # Everything should have been rolled back.
        assert product.stock == previous_stock
        assert len(cart.items) == 1
        assert Order.query.count() == 0

    def test_order_total_price(self, session, order, products):
        fetched_order = Order.query.first()
        price = order.get_total_price()
        assert fetched_order.get_total_price() == price
