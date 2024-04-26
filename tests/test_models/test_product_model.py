import pytest

from app.models import Product


class TestProductModel:
    def test_product_creation(self, session, product):
        retrieved = Product.query.first()
        assert retrieved.name == product.name
        assert retrieved.description == product.description
        assert retrieved.price == product.price
        assert retrieved.stock == product.stock

    def test_product_stock_subtraction(self, session, product):
        previous_stock = product.stock
        product.subtract_stock(10)
        session.commit()
        retrieved = Product.query.first()
        assert retrieved.stock == previous_stock - 10

    def test_product_stock_subtraction_exception(self, session, product):
        with pytest.raises(ValueError):
            product.subtract_stock(1000)
            session.commit()

    def test_product_search(self, session, product):
        retrieved = Product.search(product.name)
        assert len(retrieved) == 1
        assert retrieved[0].name == product.name
        assert retrieved[0].description == product.description
        assert retrieved[0].price == product.price
        assert retrieved[0].stock == product.stock
