def test_logout_route(test_app, client, user):
    with client:
        client.post('/login', data=dict(username='test_username', password='correct_password'),
         follow_redirects=True)
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Home' in response.data  # Redirects to the home page