from app.models import OrderItem


class TestOrderItemModel:
    def test_create_order_item(self, session, order_item):
        fetched_order_item = OrderItem.query.first()
        assert fetched_order_item.order_id == order_item.order_id
        assert fetched_order_item.product_id == order_item.product_id
        assert fetched_order_item.quantity == order_item.quantity
