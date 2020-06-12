"""
test_issues.py contains unit tests for issue related controllers.
"""
import pytest
import os
from io import BytesIO

from MasterCSS.tests.test_fixture import client

CAR_MANAGEMENT_API_URL = '/management/cars'
ISSUE_API_URL = '/issue'

def test_setup(client):
    """
    Setup issues test by registering admin user, creating an engineer,
    and a car

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
    # Creates engineer user.
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
    # Creates a car.
    with open("src/MasterCSS/tests/testImages/car1.jpg", "rb") as car1_image:
        car1_image_read = BytesIO(car1_image.read())
    response = client.post(
        CAR_MANAGEMENT_API_URL + '/add',
        data=dict(
            make="Honda Civic",
            seats="2",
            bodytype="Sedan",
            home_coordinates="(-37.812082, 144.983072)",
            fueltype="Petrol",
            colour="Blue",
            costperhour='12',
            totaldistance='0',
            numberplate="LOL123",
            image=(car1_image_read, 'car1.jpg'),
            agent_id="1"
        ),
        content_type='multipart/form-data'
    )

def test_add_issue_form(client):
    """
    Shows if it renders the form to add issue.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(ISSUE_API_URL + '/create/1')

    # Renders the correct car details
    assert b'<td>1</td>' in response.data
    assert b'<h1 class="title">Create Issue</h1>' in response.data

def test_create_issue1(client):
    """
    Adds an issue and see if it's reflected in the app.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        ISSUE_API_URL + '/create/1',
        data=dict(
            title="Example issue 1",
            description="Wheel was punctured by nail."
        ),
        follow_redirects=True
    )
    # Checks if there issue is created.
    assert b'<td>1</td>' in response.data

def test_create_issue2(client):
    """
    Adds an issue and see if it's reflected in the app.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        ISSUE_API_URL + '/create/1',
        data=dict(
            title="Example issue 2",
            description="Engine maintenance"
        ),
        follow_redirects=True
    )
    
    assert b'<td>2</td>' in response.data

def test_view_issue1(client):
    """
    Views the first issue

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(ISSUE_API_URL + '/view/1')
    # correct issue id rendered
    assert b'<td>1</td>' in response.data
    assert b'<td>Pending</td>' in response.data
    # correct car details
    assert b'<td>Honda Civic</td>' in response.data

def test_view_issue2(client):
    """
    Views the second issue

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(ISSUE_API_URL + '/view/2')
    # correct issue id rendered
    assert b'<td>2</td>' in response.data
    assert b'<td>Pending</td>' in response.data
    # correct car details
    assert b'<td>Honda Civic</td>' in response.data

def test_resolve_issue1(client):
    """
    Resolve the first issue

    :param client: Flask app client
    :type client: Flask app instance
    """

    client.get(ISSUE_API_URL + '/resolve/1')
    response = client.get(ISSUE_API_URL + '/view/1')

    # correct issue being resolved
    assert b'<td>Resolved</td>' in response.data

def test_issue2_pending(client):
    """
    Check if issue2 is still pending

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(ISSUE_API_URL + '/view/2')

    # correct issue being resolved
    assert b'<td>Pending</td>' in response.data

def test_engineer_view_pending(client):
    """
    View pending. resolved issues are not shown.

    :param client: Flask app client
    :type client: Flask app instance
    """
    client.get('/logout')
    client.post(
        '/login',
        data=dict(
            username="engineer",
            password="engineer"
        ),
        follow_redirects=True
    )
    response = client.get(ISSUE_API_URL + '/pending')

    assert b'<h1 class="title">Hey engineer these' + \
    b' are the issues still waiting for an engineer.</h1>' \
    in response.data

    # No resolved issues should be shown.
    assert b'<td>Resolved</td>' not in response.data

def test_engineer_view_issue(client):
    """
    View issue.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(ISSUE_API_URL + '/view/2')

    assert b'<td>2</td>' in response.data
    assert b'<td>Pending</td>' in response.data

def test_engineer_resolve(client):
    """
    Resolve the issue and see it render correctly.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(ISSUE_API_URL + '/resolve/2', follow_redirects=True)

    # Renders viewtaken.html
    assert b'<h1 class="title">Hey engineer these are the issues you fixed.</h1>' in response.data
    assert b'<td>2</td>' in response.data