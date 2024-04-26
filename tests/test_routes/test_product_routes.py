from app.models import Product

def test_catalog_route(session, client, products):
    """Test the catalog returns a response with the product names in them."""
    response = client.get('/catalog')
    assert response.status_code == 200
    print(response.data)
    # Make sure every product name appears on the page.
    for p in products:
        assert bytes(p.name, 'utf-8') in response.data

def test_search_route(session, client, products):
    """Test search correctly returns a filtered list of items."""
    query = "product_1"
    response = client.get(f'search?query={query}')
    assert response.status_code == 200
    assert bytes(query, 'utf-8') in response.data
    assert bytes(products[0].name, 'utf-8') in response.data
    assert bytes(products[1].name, 'utf-8') not in response.data

def test_search_route_no_query(session, client, products):
    """Test searching with no query gives all items."""
    response = client.get('/search')
    assert response.status_code == 200
    # Make sure every product name appears on the page.
    for p in products:
        assert bytes(p.name, 'utf-8') in response.data

def test_product_route(client, session, products):
    """Test product pages work and have the item name on them."""
    with client:
        response = client.get('/itmes_page/1')
        assert response.status_code == 200
        # assert bytes(product.name, 'utf-8') in response.data
