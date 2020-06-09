"""
test_user_management.py contains unit tests for user management.
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
    """
    Test admin logged in and dashboard render after test_setup registration.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'Welcome example!' in response.data

def test_admin_review_bookings_render(client):
    """
    Test admin logged in and dashboard renders Review Bookings button.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'Review bookings' in response.data

def test_admin_manage_cars_render(client):
    """
    Test admin logged in and dashboard renders Manage Cars button.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'Manage cars' in response.data

def test_admin_manage_users_render(client):
    """
    Test admin logged in and dashboard renders Manage Users button.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'Manage users' in response.data

def test_admin_view_issues_render(client):
    """
    Test admin logged in and dashboard renders View Issues button.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'View issues' in response.data

def test_admin_add_user_page(client):
    """
    Test add user page render for admin.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(USER_MANAGEMENT_API_URL + '/add')
    assert b'Add User' in response.data

def test_admin_search_user_template(client):
    """
    Test admin search user template.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(USER_MANAGEMENT_API_URL + '/search')
    assert b'<td>1</td>' in response.data
    assert b'alex' in response.data

def test_admin_add_customer(client):
    """
    Test admin add account feature: adding a customer.

    :param client: Flask app client
    :type client: Flask app instance
    """
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

def test_login_customer(client):
    """
    Test admin add account feature: logging in as customer.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="customer",
            password="customer"
        ),
        follow_redirects=True
    )

    assert b'Let\'s book you a car!' in response.data

def test_delete_customer(client):
    """
    Test admin delete account feature: deleting a customer.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password"
        ),
        follow_redirects=True
    )
    response = client.get('/users/remove/2')

    assert b'<td>2</td>' not in response.data
    assert b'customer' not in response.data

def test_login_deleted_customer(client):
    """
    Test admin delete account feature: logging in as a deleted customer.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="customer",
            password="customer"
        ),
        follow_redirects=True
    )

    assert b'User not found!' in response.data

def test_login_as_admin(client):
    """
    Test logging in as admin.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password"
        ),
        follow_redirects=True
    )

    assert b'Welcome example!' in response.data

def test_admin_add_engineer(client):
    """
    Test admin add account feature: adding an engineer.

    :param client: Flask app client
    :type client: Flask app instance
    """
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
    """
    Test admin add account feature: adding a manager.

    :param client: Flask app client
    :type client: Flask app instance
    """
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

def test_login_as_engineer(client):
    """
    Test admin add account feature: logging in as engineer.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="engineer",
            password="engineer"
        ),
        follow_redirects=True
    )

    assert b'Welcome engineer!' in response.data

def test_engineer_dashboard_render(client):
    """
    Test engineer dashboard render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')

    assert b'Get to work!' in response.data
    assert b'Your QR code' in response.data

def test_engineer_dashboard_qr_render(client):
    """
    Test engineer QR code render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')

    assert b'<img src=static/qr/' in response.data

def test_engineer_pending_issues_render(client):
    """
    Test engineer Pending Issues button render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')

    assert b'Pending issues' in response.data

def test_engineer_your_issues_render(client):
    """
    Test engineer Your Issues button render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')

    assert b'Your issues' in response.data

def test_login_as_manager(client):
    """
    Test admin add account feature: logging in as manager.

    :param client: Flask app client
    :type client: Flask app instance
    """
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

def test_manager_dashboard_render(client):
    """
    Test manager dashboard render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'Welcome manager!' in response.data

def test_manager_daily_revenue_graph_render(client):
    """
    Test manager daily revenue graph render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'<iframe name="daily_revenue_graph"' in response.data

def test_manager_total_bookings_car_graph_render(client):
    """
    Test manager total bookings of all cars graph render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'<iframe name="total_bookings_car_graph"' in response.data

def test_manager_daily_active_user_graph_render(client):
    """
    Test manager daily active users graph render.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/')
    assert b'<iframe name="daily_active_user_graph"' in response.data

def test_delete_engineer(client):
    """
    Test admin delete account feature: deleting an engineer.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password"
        ),
        follow_redirects=True
    )
    response = client.get('/users/remove/3')

    assert b'<td>3</td>' not in response.data
    assert b'engineer' not in response.data

def test_login_deleted_engineer(client):
    """
    Test admin delete account feature: logging in as a deleted engineer.

    :param client: Flask app client
    :type client: Flask app instance
    """
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

def test_delete_manager(client):
    """
    Test admin delete account feature: deleting a manager.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password"
        ),
        follow_redirects=True
    )
    response = client.get('/users/remove/4')

    assert b'<td>4</td>' not in response.data
    assert b'manager' not in response.data

def test_login_deleted_manager(client):
    """
    Test admin delete account feature: logging in as a deleted manager.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="manager",
            password="manager"
        ),
        follow_redirects=True
    )

    assert b'User not found!' in response.data

def test_delete_admin_self(client):
    """
    Test admin delete account feature: deleting admin oneself (shouldn't work)

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password"
        ),
        follow_redirects=True
    )
    response = client.get('/users/remove/1')

    assert b'<td>1</td>' in response.data
    assert b'example' in response.data

def test_admin_add_admin(client):
    """
    Test admin add account feature: adding another admin.

    :param client: Flask app client
    :type client: Flask app instance
    """
    with open("src/MasterCSS/tests/" +
              "testImages/example.jpg", "rb") as user_image:
        user_image_read = BytesIO(user_image.read())

    response = client.post(
        '/register',
        data=dict(
            username="admin2",
            password="admin2",
            email="admin2@admin2.com",
            firstname="admin2",
            lastname="admin2",
            phonenumber="01231234567890",
            usertype="ADMIN",
            image=(user_image_read, 'example.jpg')
        ),
        follow_redirects=True
    )

    # Should render the new user's details
    assert b'<td>5</td>' in response.data
    assert b'admin2' in response.data

def test_delete_admin_other(client):
    """
    Test admin delete account feature: deleting other admin

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/users/remove/5')

    assert b'<td>5</td>' not in response.data
    assert b'admin2' not in response.data

def test_login_deleted_admin(client):
    """
    Test admin delete account feature: logging in as a deleted admin.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    response = client.post(
        '/login',
        data=dict(
            username="admin2",
            password="admin2"
        ),
        follow_redirects=True
    )

    assert b'User not found!' in response.data
