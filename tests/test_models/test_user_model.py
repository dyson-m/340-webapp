from flask_login import LoginManager, login_user, logout_user, current_user
import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Cart, User


class TestUserModel:
    def test_create_user(self, session, user):
        fetched_user = user.query.filter(User.email == user.email).first()
        assert fetched_user.name == user.name
        assert fetched_user.email == user.email
        assert fetched_user.address == user.address

    def test_user_unique_email(self, session, user):
        user2 = User(name=user.name, email=user.email, address=user.address)
        session.add(user2)
        with pytest.raises(IntegrityError):
            session.commit()

    def test_user_password(self, session, user):
        user.set_password("correct_password")
        fetched_user = user.query.filter(User.email == user.email).first()
        assert fetched_user.check_password("correct_password")
        assert not fetched_user.check_password('wrong_password')

    def test_update_user_info(self, session, user):
        old_email = user.email
        user.update_user_info(name="new_name", address="new_address")
        fetched_user = user.query.filter(User.email == old_email).first()
        assert fetched_user.name == "new_name"
        assert fetched_user.email == old_email
        assert fetched_user.address == "new_address"

    def test_user_cart(self, session, user):
        cart = Cart(user=user)
        session.add(cart)
        session.commit()

        fetched_cart = Cart.query.filter(Cart.user_id == user.id).first()
        assert fetched_cart.id == user.cart.id
        assert fetched_cart.user_id == user.id

    def test_user_cart_deletion(self, session, user, cart):
        assert cart.query.filter(Cart.user_id == user.id).first() is not None

        session.delete(user)
        session.commit()

        assert cart.query.filter(Cart.user_id == user.id).first() is None

    def test_user_admin(self, session, user, admin):
        fetched_user = user.query.filter(User.email == user.email).first()
        fetched_admin = admin.query.filter(User.email == admin.email).first()
        assert not fetched_user.is_admin
        assert fetched_admin.is_admin

    def test_auto_id_increments(self, session, user, admin):
        assert user.id == 1
        assert admin.id == 2

        session.delete(user)

        new_user = User(name="new_user", email="new_email",
                        address="new_address")
        session.add(new_user)
        session.commit()

        assert new_user.id == 3

        session.delete(new_user)
        session.commit()

        new_user2 = User(name="new_user2", email="new_email2",
                            address="new_address2")
        session.add(new_user2)
        session.commit()

        assert new_user2.id == 3

    def test_get_user_by_email(self, session, user):
        fetched_user = User.get_user_by_email(user.email)
        assert fetched_user.email == user.email
        failed_user = User.get_user_by_email("fake_email")
        assert failed_user is None
