"""
test_car.py contains unit tests for car controllers.
"""
import pytest
import os
from io import BytesIO

from datetime import datetime

from MasterCSS.tests.test_fixture import client

CAR_MANAGEMENT_API_URL = '/management/cars'
BOOKING_API_URL = '/booking'
CAR_API_URL = '/cars'

HTML_DATETIME_FORMAT = '%d/%m/%Y %H:%M'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

PICKUP_DATE = datetime(2021, 5, 17)
RETURN_DATE = datetime(2021, 5, 18)

PICKUP_AND_RETURN = PICKUP_DATE.strftime(HTML_DATETIME_FORMAT) + " - "\
    + RETURN_DATE.strftime(HTML_DATETIME_FORMAT)


def test_setup(client):
    """
    Setup car test by registering user and add cars.

    :param client: Flask app client
    :type client: Flask app instance
    """
    # Register user (includes login)
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

    # Add 2 cars
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


def test_filter_cars(client):
    """
    Filter available cars with valid date time.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_API_URL + '/filter',
        data=dict(
            datetimes=PICKUP_AND_RETURN
        ),
        content_type='multipart/form-data'
    )

    # Checks correct template rendered
    assert b'Congrats!' in response.data

    # Checks if the date time is captured properly
    assert b'<code>' + str.encode(PICKUP_DATE.strftime(DEFAULT_DATETIME_FORMAT)) + b'</code> to <code>' \
        + str.encode(RETURN_DATE.strftime(DEFAULT_DATETIME_FORMAT)
                     ) + b'</code>' in response.data

    # Test if the previously added cars exists.
    assert b'Honda CR-V' in response.data
    assert b'Honda Civic' in response.data


def test_filter_invalid(client):
    """
    Filter cars with invalid datetime.

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_API_URL + '/filter',
        data=dict(
            datetimes="19/06/2020 20:00 - 17/06/2020 03:00"
        ),
        content_type='multipart/form-data'
    )

    # Checks if Err message is rendered.
    assert b'Invalid date range! Please try again.' in response.data


def test_search_make(client):
    """
    Search cars based on make

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_API_URL + '/search',
        data=dict(
            make="Honda Civic",
            seats="Any",
            fueltype="Any",
            colour="Any",
            pickup_coordinates="Any",
            bodytype="Any",
            pickup_time=PICKUP_DATE,
            return_time=RETURN_DATE
        )
    )

    assert b'Honda Civic' in response.data
    assert b'Honda CR-V' not in response.data


def test_search_location(client):
    """
    Search cars based on locations

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_API_URL + '/search',
        data=dict(
            make="",
            seats="Any",
            fueltype="Any",
            colour="Any",
            pickup_coordinates="(-37.806708, 144.968947)",
            bodytype="Any",
            pickup_time=PICKUP_DATE,
            return_time=RETURN_DATE
        )
    )

    assert b'Honda Civic' not in response.data
    assert b'Honda CR-V' in response.data


def test_search_not_found(client):
    """
    Search car that doesn't exist

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_API_URL + '/search',
        data=dict(
            make="Hahaha",
            seats="100",
            fueltype="Sunlight",
            colour="Transparent",
            pickup_coordinates="(1, 1)",
            bodytype="Big foot",
            pickup_time=PICKUP_DATE,
            return_time=RETURN_DATE
        )
    )

    assert b'Honda Civic' not in response.data
    assert b'Honda CR-V' not in response.data


def test_search(client):
    """
    Search car with more than one fields as parameter

    :param client: Flask app client
    :type client: Flask app instance
    """
    response = client.post(
        CAR_API_URL + '/search',
        data=dict(
            make="",
            seats="Any",
            fueltype="Diesel",
            colour="Red",
            pickup_coordinates="(-37.806708, 144.968947)",
            bodytype="SUV",
            pickup_time=PICKUP_DATE,
            return_time=RETURN_DATE
        )
    )

    assert b'Honda Civic' not in response.data
    assert b'Honda CR-V' in response.data


def test_filter_after_book(client):
    """
    Filter car after book. booked car should not be seen.

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

    response = client.post(
        CAR_API_URL + '/filter',
        data=dict(
            datetimes=PICKUP_AND_RETURN
        ),
        content_type='multipart/form-data'
    )

    assert b'Honda CR-V' in response.data
    assert b'Honda Civic' not in response.data
