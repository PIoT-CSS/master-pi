"""
test_user_management.py contains unit tests for user management.
Tests related to controllers under /mangement/cars which is used to manage
car entries in db.
"""

"""
test_car.py contains unit tests for car management.
Tests related to controllers under /mangement/cars which is used to manage
car entries in db.
"""
import pytest
import os
from io import BytesIO

from MasterCSS.tests.test_fixture import client

USER_MANAGEMENT_API_URL = '/users'

def test_setup(client):
    """
    Setup car test by registering user and add cars.

    :param client: Flask app client
    :type client: Flask app instance
    """
    # Register an admin user (includes login)
    with open("src/MasterCSS/tests/" +
              "testImages/example.jpg", "rb") as user_image:
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
            usertype="ADMIN",
            image=(user_image_read, 'example.jpg')
        )
    )

def test_logged_in_admin(client):
    response = client.get('/')
    assert b'Review bookings' in response.data
    assert b'Manage cars' in response.data
    assert b'Manage users' in response.data
    assert b'View issues' in response.data

def test_admin_add_user_page(client):
    """
    Route renders correct form.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(USER_MANAGEMENT_API_URL + '/add')
    assert b'Add User' in response.data

def test_admin_search_user_template(client):
    response = client.get(USER_MANAGEMENT_API_URL + '/search')
    assert b'<td>1</td>' in response.data
    assert b'alex' in response.data

def test_admin_add_customer(client):
    with open("src/MasterCSS/tests/" +
              "testImages/example.jpg", "rb") as user_image:
        user_image_read = BytesIO(user_image.read())

    response = client.post(
        '/register',
        data=dict(
            username="customer",
            password="customer",
            email="customer@customer.com",
            firstname="customer",
            lastname="customer",
            phonenumber="1234567890",
            usertype="CUSTOMER",
            image=(user_image_read, 'example.jpg')
        ),
        follow_redirects=True
    )

    # Should render the new user's details
    assert b'<td>2</td>' in response.data
    assert b'customer' in response.data

def test_admin_add_engineer(client):
    with open("src/MasterCSS/tests/" +
              "testImages/example.jpg", "rb") as user_image:
        user_image_read = BytesIO(user_image.read())

    response = client.post(
        '/register',
        data=dict(
            username="engineer",
            password="engineer",
            email="engineer@engineer.com",
            firstname="engineer",
            lastname="engineer",
            phonenumber="1234567190",
            usertype="ENGINEER",
            macaddress="10:10:10:10:10",
            image=(user_image_read, 'example.jpg')
        ),
        follow_redirects=True
    )

    # Should render the new user's details
    assert b'<td>3</td>' in response.data
    assert b'engineer' in response.data

def test_admin_add_manager(client):
    with open("src/MasterCSS/tests/" +
              "testImages/example.jpg", "rb") as user_image:
        user_image_read = BytesIO(user_image.read())

    response = client.post(
        '/register',
        data=dict(
            username="manager",
            password="manager",
            email="manager@manager.com",
            firstname="manager",
            lastname="manager",
            phonenumber="123578123",
            usertype="MANAGER",
            image=(user_image_read, 'example.jpg')
        ),
        follow_redirects=True
    )

    # Should render the new user's details
    assert b'<td>4</td>' in response.data
    assert b'manager' in response.data

def test_delete_user(client):
    response = client.get('/remove/2')
    assert b'<td>2</td>' not in response.data
    assert b'customer' not in response.data

def test_login_deleted_user(client):
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="engineer",
            password="engineer"
        ),
        follow_redirects=True
    )

    assert b'User not found!' in response.data

def test_login_as_engineer(client):
    response = client.post(
        '/login',
        data=dict(
            username="engineer",
            password="engineer"
        ),
        follow_redirects=True
    )

    assert b'Welcome engineer!' in response.data

def test_login_as_manager(client):
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="manager",
            password="manager"
        ),
        follow_redirects=True
    )

    assert b'Welcome manager!' in response.data