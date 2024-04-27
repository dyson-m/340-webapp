from app.models import Order


def test_checkout_no_cart(session, client, user):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        response = client.get('/checkout', follow_redirects=True)
        print(response.data)
        assert response.status_code == 200
        assert b'Your cart is empty.' in response.data

def test_checkout_empty_cart(session, client, user, cart):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        session.add(cart)
        session.commit()
        response = client.get('/checkout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Your cart is empty.' in response.data

def test_checkout_items_in_cart(session, client, user, cart, product):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        cart.add_product(product.id, 2)
        session.add(cart)
        session.commit()
        response = client.get('/checkout', follow_redirects=True)
        assert response.status_code == 200
        assert b'test_product' in response.data
        assert b'5.99' in response.data
        assert b'2' in response.data
        assert b'$11.98' in response.data

def test_checkout_submit_success(session, client, user, cart, product):
    with client:
        previous_product_stock = product.stock
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        cart.add_product(product.id, 2)
        session.commit()
        response = client.post('/checkout', data={
            'name': user.name,
            'address': user.address,
            'card_type': 'visa',
            'card_number': '1234567890123456',
            'exp_month': '1',
            'exp_year': '2032',
            'cvv': '123'
        }, follow_redirects=True)
        assert b'Order placed successfully.' in response.data
        new_order = Order.query.filter_by(user_id=user.id).first()
        new_product_stock = product.stock
        # Check order has correct items.
        assert new_order.items[0].product_id == product.id
        assert new_order.items[0].quantity == 2
        # Check product stock has been updated.
        assert new_product_stock == previous_product_stock - 2
        # Check cart has been emptied.
        assert len(cart.items) == 0
