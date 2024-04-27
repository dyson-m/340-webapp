def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

    response = client.get('/index')
    assert response.status_code == 200
    assert b'Home' in response.data