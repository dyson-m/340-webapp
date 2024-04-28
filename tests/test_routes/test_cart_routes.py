def test_cart_route(session, client, user, cart, product):
    """Test the cart route returns a page with the product info in it."""
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        cart.add_product(product.id, 2)
        session.add(cart)
        session.commit()
        response = client.get('/cart')
        assert response.status_code == 200
        assert b'test_product' in response.data
        assert b'5.99' in response.data
        assert b'2' in response.data
        assert b'$11.98' in response.data

def test_cart_route_no_cart(session, client, user):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        response = client.get('/cart')
        # TODO: Should not having a cart be a 404, or should it create a cart?
        assert response.status_code == 404

def test_cart_empty_cart(session, client, user, cart):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        session.add(cart)
        session.commit()
        response = client.get('/cart')
        assert response.status_code == 200
        assert b'Your cart is currently empty.' in response.data

def test_add_to_cart(session, client, user, cart, product):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        assert len(cart.items) == 0
        response = client.post(f'/add_to_cart/{product.id}',
                               data=dict(quantity=2),
                               follow_redirects=True)
        assert response.status_code == 200
        assert cart.items[0].product.id == product.id
        assert cart.items[0].quantity == 2

def test_remove_from_cart(session, client, user, cart, product):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        cart.add_product(product.id, 2)
        session.add(cart)
        session.commit()
        assert len(cart.items) == 1
        response = client.post(f'/remove_from_cart/{product.id}',
                               follow_redirects=True)
        assert response.status_code == 200
        assert len(cart.items) == 0

def test_update_cart_item(session, client, user, cart, product):
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        cart.add_product(product.id, 2)
        session.add(cart)
        session.commit()
        assert cart.items[0].quantity == 2
        response = client.post(f'/update_cart_item/{product.id}',
                               data=dict(quantity=5),
                               follow_redirects=True)
        assert response.status_code == 200
        assert cart.items[0].quantity == 5
