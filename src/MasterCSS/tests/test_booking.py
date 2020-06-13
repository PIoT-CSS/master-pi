"""
test_booking.py contains unit tests for booking.
"""
import pytest
import os
from io import BytesIO

from datetime import datetime

from MasterCSS.tests.test_fixture import client

CAR_MANAGEMENT_API_URL = '/management/cars'
BOOKING_API_URL = '/booking'

HTML_DATETIME_FORMAT = '%d/%m/%Y %H:%M'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

PICKUP_DATE = datetime(2021, 5, 17)
RETURN_DATE = datetime(2021, 5, 18)

PICKUP_AND_RETURN = PICKUP_DATE.strftime(HTML_DATETIME_FORMAT) + " - "\
    + RETURN_DATE.strftime(HTML_DATETIME_FORMAT)

# Setup booking test by registering user and add cars.


def test_setup(client):
    """
    Setup booking test by registering user and add cars.

    :param client: Flask app client
    :type client: Flask app instance
    """
    # Register user (includes login)
    with open("src/MasterCSS/tests/testImages/" + \
                "example.jpg", "rb") as user_image:
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

    # Add 2 cars
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

    with open("src/MasterCSS/tests/testImages/car2.jpg", "rb") as car2_image:
        car2_image_read = BytesIO(car2_image.read())
    client.post(
        CAR_MANAGEMENT_API_URL + '/add',
        data=dict(
            make="Honda Civic",
            seats="2",
            fueltype="Diesel",
            bodytype="Sedan",
            home_coordinates="(-37.812082, 144.983072)",
            colour="Blue",
            costperhour='12',
            totaldistance='0',
            numberplate="BAB111",
            image=(car2_image_read, 'car1.jpg'),
            agent_id="2"
        ),
        content_type='multipart/form-data'
    )


def test_view_car_booking(client):
    """
    Test view booking details when the car is available.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        BOOKING_API_URL + '/book',
        data=dict(
            pickup_datetime=PICKUP_DATE,
            return_datetime=RETURN_DATE,
            car_id=1,
        ),
        content_type='multipart/form-data'
    )

    assert b'Available!' in response.data


def test_confirm_booking(client):
    """
    Test confirm booking should show booking confirmed message.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        BOOKING_API_URL + '/confirm',
        data=dict(
            pickup_datetime=PICKUP_DATE,
            return_datetime=RETURN_DATE,
            car_id=1,
        ),
        content_type='multipart/form-data'
    )

    assert response.status_code == 200
    assert b'Your booking has been confirmed, thank you!' in response.data


def test_booking_in_mybookings(client):
    """
    Test confirmed booking details should appear in mybookings.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.get('/mybookings')

    assert str.encode(PICKUP_DATE.strftime(
        DEFAULT_DATETIME_FORMAT)) in response.data
    assert str.encode(RETURN_DATE.strftime(
        DEFAULT_DATETIME_FORMAT)) in response.data
    assert b'1' in response.data
    assert b'Confirmed' in response.data


def test_cancel_booking(client):
    """
    Test cancel is successful.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        BOOKING_API_URL + '/cancel',
        data=dict(
            booking_id=1
        ),
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert b'Confirmed' not in response.data
    # Make sure cancel button is not rendered
    assert b'button is-danger' not in response.data
    assert b'Canceled' in response.data


def test_view_booking(client):
    """
    Test view booking is showing correct booking information.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        BOOKING_API_URL + '/view',
        data=dict(
            booking_id=1
        ),
        content_type='multipart/form-data'
    )

    assert b'Booking ID: 1' in response.data
    assert b'Car ID: </strong> 1' in response.data
    assert b'User ID: </strong> 1' in response.data
    assert b'Pickup time: </strong> ' + \
        str.encode(PICKUP_DATE.strftime(
            DEFAULT_DATETIME_FORMAT)) in response.data
    assert b'Return time: </strong> ' + \
        str.encode(RETURN_DATE.strftime(
            DEFAULT_DATETIME_FORMAT)) in response.data
    assert b'Canceled' in response.data  # previous test canceled this booking.
