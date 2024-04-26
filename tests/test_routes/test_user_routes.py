from app.models import User

def test_login_route(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_logout_route(client, user):
    with client:
        client.post('/login', data=dict(username='test_username', password='correct_password'),
         follow_redirects=True)
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Home' in response.data

def test_login_success(client, user):
    response = client.post('/login', data=dict(username='test_username',
                                               password='correct_password'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Home' in response.data

def test_login_failure(client, user):
    response = client.post('/login', data=dict(username='test_username',
                                               password='incorrect_password'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    # assert an error is shown:
    # assert b'Invalid username or password' in response.data

def test_register_route(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_success(client):
    response = client.post('/register',
                           data=dict(username='new_username',
                                     password='new_password',
                                     password2='new_password'),
                           follow_redirects=True)
    new_user = User.query.filter_by(username='new_username').first()
    assert new_user is not None
    assert response.status_code == 200
    assert b'Login' in response.data

