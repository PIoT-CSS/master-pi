"""
test_car.py contains unit tests for car management.
Tests related to controllers under /mangement/cars which is used to manage car entries in db.
"""
import pytest
import os
from io import BytesIO

from MasterCSS.tests.test_fixture import client

CAR_MANAGEMENT_API_URL = '/management/cars'


def test_add_car(client):
    """
    Test adding 2 cars into system to populate data.

    :param client: Flask app client
    :type client: Flask app instance
    """
    with open("src/MasterCSS/tests/testImages/car1.jpg", "rb") as car1_image:
        car1_image_read = BytesIO(car1_image.read())
    response = client.post(
        CAR_MANAGEMENT_API_URL + '/add',
        data=dict(
            secretkey=os.getenv('SECRET_KEY'),
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

    with open("src/MasterCSS/tests/testImages/car2.jpg", "rb") as car2_image:
        car2_image_read = BytesIO(car2_image.read())
    client.post(
        CAR_MANAGEMENT_API_URL + '/add',
        data=dict(
            secretkey=os.getenv('SECRET_KEY'),
            make="Honda CR-V",
            seats="4",
            fueltype="Diesel",
            bodytype="SUV",
            home_coordinates="(-37.806708, 144.968947)",
            colour="Red",
            costperhour='18',
            totaldistance='0',
            numberplate="BAB111",
            image=(car2_image_read, 'car2.jpg'),
            agent_id="2"
        ),
        content_type='multipart/form-data'
    )


def test_view_all_cars(client):
    """
    Test view all cars: should contain the 2 cars added in the previous test.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(
        CAR_MANAGEMENT_API_URL
    )

    assert b'LOL123' in response.data
    assert b'BAB111' in response.data


def test_view_first_car(client):
    """
    Test viewing details of the first car.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(
        CAR_MANAGEMENT_API_URL + '/1'
    )

    assert b'LOL123' in response.data

# Change the details of the car


def test_change_car_detail(client):
    """
    Test changing details of a car

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_MANAGEMENT_API_URL + '/1/modify',
        data=dict(
            secretkey=os.getenv('SECRET_KEY'),
            make="Honda Civic",
            seats="2",
            bodytype="Sedan",
            fueltype="Diesel",
            home_coordinates="(-37.812082, 144.983072)",
            colour="Blue",
            costperhour='12',
            totaldistance='0',
            numberplate="AHA456",
            agent_id="2",
            follow_redirect=True
        ),
        follow_redirects=True
    )

    assert b'AHA456' in response.data


def test_remove_car(client):
    """
    Test removing the first car added

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get(
        CAR_MANAGEMENT_API_URL + '/1/remove'
    )

    assert b'AHA456' not in response.data
