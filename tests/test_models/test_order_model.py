from app.models import Order


class TestOrderModel:
    def test_order_creation(self, session, order, products):
        fetched_order = Order.query.first()
        assert fetched_order.user_id == order.user_id
        assert fetched_order.get_total_price() == order.get_total_price()
        assert fetched_order.items[0].product_id == products[0].id
        assert fetched_order.items[1].product_id == products[1].id

    def test_order_creation_from_cart(self, session, order, cart, products):
        new_order = Order.create_order_from_cart(cart)
        session.add(new_order)
        session.commit()

        fetched_order = Order.query.filter(Order.user_id == cart.user.id
                                           ).first()
        assert fetched_order.user_id == cart.user.id
        assert fetched_order.get_total_price() == cart.get_total_price()

    def test_order_total_price(self, session, order, products):
        fetched_order = Order.query.first()
        price = order.get_total_price()
        assert fetched_order.get_total_price() == price
