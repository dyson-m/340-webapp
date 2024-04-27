"""Test access to the admin dashboard, ability to delete users, and
the sales report."""
from app.models import User


def test_admin_page_success(session, client, admin):
    """Test that an admin user can access the admin page."""
    with client:
        # Login as an admin user.
        client.post('/login', data=dict(username='test_admin_username',
                                        password='password'),
                    follow_redirects=True)
        response = client.get('/admin', follow_redirects=True)
        assert response.status_code == 200


def test_admin_page_401(client):
    """Test that an anonymous user can't access the admin page."""
    with client:
        # Don't log in as any user
        response = client.get('/admin', follow_redirects=True)
        assert response.status_code == 401


def test_admin_page_403(session, client, user):
    """Test a basic user can't access the admin page."""
    with client:
        # Login as a basic user
        client.post('/login', data=dict(username='test_username',
                                        password='correct_password'),
                    follow_redirects=True)
        response = client.get('/admin', follow_redirects=True)
        assert response.status_code == 403


def test_admin_delete_user(session, client, admin, user):
    """Test that an admin user can delete a user."""
    with client:
        # Login as an admin user.
        client.post('/login', data=dict(username='test_admin_username',
                                        password='password'),
                    follow_redirects=True)

        # Check that user exists before deleting.
        assert session.get(User, 1) is not None

        response = client.post('/admin', data=dict(user=1),
                               follow_redirects=True)
        assert response.status_code == 200
        # Check that the user was deleted.
        assert session.get(User, 1) is None


def test_sales_report(session, client, admin, order):
    """Test sales report returns a csv file with the order data."""
    with client:
        # Login as an admin user.
        client.post('/login', data=dict(username='test_admin_username',
                                        password='password'),
                    follow_redirects=True)
        response = client.get('/admin/sales_report', follow_redirects=True)
        assert (response.headers['Content-Disposition'] ==
                'attachment; filename=orders.csv')
        # TODO: This could be more comprehensive.
        # Just checking it has the right idea.
        assert response.status_code == 200
        assert bytes(str(order.items[0].id), 'utf-8') in response.data
        assert b'order_date' in response.data
        date = order.order_date.strftime('%Y-%m-%d')
        assert bytes(date, 'utf-8') in response.data

