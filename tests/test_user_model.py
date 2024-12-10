import pytest
from sqlalchemy.exc import IntegrityError
from weather.db import db
from weather.models.user_model import Users

@pytest.fixture
def setup_test_db(app):
    """
    Fixture to set up a clean database for testing.
    """
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_create_user_success(setup_test_db):
    """
    Test successful creation of a user.
    """
    Users.create_user("test_user", "secure_password")
    user = Users.query.filter_by(username="test_user").first()

    assert user is not None, "User should exist in the database"
    assert user.username == "test_user", "Username should match the created user"


def test_create_user_duplicate(setup_test_db):
    """
    Test creating a user with a duplicate username.
    """
    Users.create_user("test_user", "secure_password")
    with pytest.raises(ValueError, match="User with username 'test_user' already exists"):
        Users.create_user("test_user", "another_password")


def test_check_password_success(setup_test_db):
    """
    Test successful password verification.
    """
    Users.create_user("test_user", "secure_password")
    assert Users.check_password("test_user", "secure_password") is True, "Password should match"


def test_check_password_failure(setup_test_db):
    """
    Test password verification with incorrect password.
    """
    Users.create_user("test_user", "secure_password")
    assert Users.check_password("test_user", "wrong_password") is False, "Password should not match"


def test_check_password_user_not_found(setup_test_db):
    """
    Test password verification for a non-existent user.
    """
    with pytest.raises(ValueError, match="User test_user not found"):
        Users.check_password("test_user", "secure_password")


def test_delete_user_success(setup_test_db):
    """
    Test successful deletion of a user.
    """
    Users.create_user("test_user", "secure_password")
    Users.delete_user("test_user")
    user = Users.query.filter_by(username="test_user").first()

    assert user is None, "User should be deleted from the database"


def test_delete_user_not_found(setup_test_db):
    """
    Test deletion of a non-existent user.
    """
    with pytest.raises(ValueError, match="User test_user not found"):
        Users.delete_user("test_user")


def test_update_password_success(setup_test_db):
    """
    Test successful password update.
    """
    Users.create_user("test_user", "secure_password")
    Users.update_password("test_user", "new_password")
    assert Users.check_password("test_user", "new_password") is True, "Password should be updated"


def test_update_password_user_not_found(setup_test_db):
    """
    Test updating the password for a non-existent user.
    """
    with pytest.raises(ValueError, match="User test_user not found"):
        Users.update_password("test_user", "new_password")


def test_get_id_by_username_success(setup_test_db):
    """
    Test retrieving user ID by username.
    """
    Users.create_user("test_user", "secure_password")
    user_id = Users.get_id_by_username("test_user")
    user = Users.query.get(user_id)

    assert user is not None, "User should exist"
    assert user.username == "test_user", "Username should match"


def test_get_id_by_username_not_found(setup_test_db):
    """
    Test retrieving user ID for a non-existent username.
    """
    with pytest.raises(ValueError, match="User test_user not found"):
        Users.get_id_by_username("test_user")