import pytest
import os
from io import BytesIO

from MasterCSS.tests.test_fixture import client

CAR_MANAGEMENT_API_URL = '/management/cars'
BOOKING_API_URL = '/booking'

# Setup booking test by registering user and add cars.
def test_setup(client):
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

# Test view booking details when the car is available.
def test_view_booking(client):
    response = client.post(
        BOOKING_API_URL + '/book',
        data=dict(
            pickup_datetime="2020-05-18 17:00:00",
            return_datetime="2020-05-23 00:00:00",
            car_id=1,
        ),
        content_type='multipart/form-data'
    )

    assert b'Available!' in response.data

# Test confirm booking should show booking confirmed message.
def test_confirm_booking(client):
    response = client.post(
        BOOKING_API_URL + '/confirm',
        data=dict(
            pickup_datetime="2020-05-18 17:00:00",
            return_datetime="2020-05-23 00:00:00",
            car_id=1,
        ),
        content_type='multipart/form-data'
    )

    assert response.status_code == 200
    assert b'Your booking has been confirmed, thank you!' in response.data

# Test confirmed booking details should appear in mybookings.
def test_booking_in_mybookings(client):
    response = client.get('/mybookings')

    assert b'2020-05-18 17:00:00' in response.data
    assert b'2020-05-23 00:00:00' in response.data
    assert b'1' in response.data
    assert b'Confirmed' in response.data

# Test cancel is successful.
def test_cancel_booking(client):
    response = client.post(
        BOOKING_API_URL + '/cancel',
        data=dict(
            booking_id=1
        ),
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert b'Confirmed' not in response.data
    assert b'button is-danger' not in response.data # Make sure cancel button is not rendered
    assert b'Canceled' in response.data

# Test view booking is showing correct booking information.
def test_view_booking(client):
    response = client.post(
        BOOKING_API_URL + '/view',
        data=dict(
            booking_id=1
        ),
        content_type='multipart/form-data'
    )

    assert b'Booking ID: 1' in response.data
    assert b'Car ID: 1' in response.data
    assert b'User ID: 1' in response.data
    assert b'Pickup time: 2020-05-18 17:00:00' in response.data
    assert b'Return time: 2020-05-23 00:00:00' in response.data
    assert b'Status: Canceled' in response.data