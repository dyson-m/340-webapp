"""These tests check that the routes provide the expected response and
that user login, logout, and registration all operate correctly."""
import flask

from app.models import User

def test_login_route(client):
    """Test the login route returns a page with Login in the body."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_logout_route(session, client, user):
    """Test the logout route redirects to the home page."""
    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
         follow_redirects=True)
        # Check they are logged in before logging them out.
        assert user is not None
        assert user.id == int(flask.session['_user_id'])
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Home' in response.data
        # Check that they were logged out fully
        assert '_user_id' not in flask.session


def test_login_success(session, client, user):
    """Test the login page redirects to the home page when
    and the user is logged in."""
    response = client.post('/login', data=dict(username='test_username',
                                               password='correct_password'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Home' in response.data

    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'))
        assert user is not None
        assert user.id == int(flask.session['_user_id'])


def test_login_failure(client, user):
    """Test the login page returns the login page when the user fails
    to enter the right password, and that the user is not logged in."""
    response = client.post('/login', data=dict(username='test_username',
                                               password='incorrect_password'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    # assert an error is shown:
    # assert b'Invalid username or password' in response.data

    with client:
        client.post('/login', data=dict(username='test_username',
                                        password='incorrect_password'))
        assert '_user_id' not in flask.session


def test_register_route(client):
    """Test register route returns a page with Register in the body"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_success(client):
    """Test registration page can successfully add a user to the database."""
    response = client.post('/register',
                           data=dict(username='new_username',
                                     password='new_password',
                                     password2='new_password'),
                           follow_redirects=True)
    new_user = User.query.filter_by(username='new_username').first()
    assert new_user is not None
    assert response.status_code == 200
    assert b'Login' in response.data

