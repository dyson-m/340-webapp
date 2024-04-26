from app.models import CartItem


class TestCartItemModel:
    def test_create_cart_item(self, session, cart_item):
        fetched_cart_item = CartItem.query.first()
        assert fetched_cart_item.cart_id == cart_item.cart_id
        assert fetched_cart_item.product_id == cart_item.product_id
        assert fetched_cart_item.quantity == cart_item.quantity

    def test_update_quantity(self, session, cart_item):
        cart_item.update_quantity(10)
        session.commit()
        fetched_cart_item = CartItem.query.first()
        assert fetched_cart_item.quantity == 10