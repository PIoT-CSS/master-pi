"""
test_auth.py contains unit tests for authentication.
"""
import pytest
from io import BytesIO
from http import HTTPStatus
from MasterCSS.tests.test_fixture import client


def test_render_register(client):
    """
    Route renders register.html when not logged in

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/register')
    assert b'Register' in response.data


def test_render_login(client):
    """
    Route renders login.html when not logged in

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/login')
    assert b'Login' in response.data


def test_render_index(client):
    """
    Route renders index.html when not logged in

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'Welcome to Car Share System!' in response.data


def test_404_not_found(client):
    """
    Route to route that doesn't exist, renders the 404 template.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/asdfadfasdf')
    assert b'404 Not Found' in response.data
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_unauthorised(client):
    """
    Test unauthorised access to auth-secured pages when not logged in

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/myinfo')
    assert b'Unauthorised' in response.data
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client.get('/mybookings')
    assert b'Unauthorised' in response.data
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_register_invalid(client):
    """
    Test register with invalid values

    :param client: Flask app client
    :type client: Flask app instance
    """
    with open("src/MasterCSS/tests/testImages/example.jpg", "rb") as user_image:
        user_image_read = BytesIO(user_image.read())
    response = client.post(
        '/register',
        data=dict(
            username="a",
            password="a",
            email="a@a.com",
            firstname="a",
            lastname="a",
            phonenumber="a",
            image=(user_image_read, 'example.jpg')
        )
    )
    assert b'Invalid' in response.data

# Test register with valid values


def test_register_valid(client):
    """
    Test register with valid values

    :param client: Flask app client
    :type client: Flask app instance
    """
    with open("src/MasterCSS/tests/testImages/example.jpg", "rb") as user_image:
        user_image_read = BytesIO(user_image.read())
    response = client.post(
        '/register',
        data=dict(
            username="example",
            password="password",
            email="example@example.com",
            firstname="alex",
            lastname="witedja",
            phonenumber="04325672682",
            image=(user_image_read, 'example.jpg')
        )
    )
    assert response.status_code == 302

# Test logout feature


def test_logout(client):
    """
    Test logout feature

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/logout', follow_redirects=True)
    assert b'Welcome to Car Share System!' in response.data


def test_login_unregistered(client):
    """
    Test login with unregistered user

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        '/login',
        data=dict(
            username="example1",
            password="password1"
        ),
        follow_redirects=True
    )
    assert b'User not found!' in response.data


def test_login_invalid(client):
    """
    Test login with invalid password

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password1"
        ),
        follow_redirects=True
    )
    assert b'Password mismatch!' in response.data


def test_login_valid(client):
    """
    Test login with registered user

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password",
            follow_redirect=True
        ),
        follow_redirects=True
    )
    assert b'Let\'s book you a car!' in response.data


def test_dashboard_route(client):
    """
    Test dashboard route after logged in

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(
        '/'
    )

    assert b'Let\'s book you a car!' in response.data
