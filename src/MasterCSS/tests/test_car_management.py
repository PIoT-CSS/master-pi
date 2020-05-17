import pytest
import os
from io import BytesIO

from MasterCSS.tests.test_fixture import client

CAR_MANAGEMENT_API_URL = '/management/cars'

# Tests related to controllers under /mangement/cars which is used to manage car entries in db.
# Adding 2 cars to populate data
def test_add_car(client):
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

# View all cars should contain the 2 cars added in the previous test.
def test_view_all_cars(client):
    response = client.get(
        CAR_MANAGEMENT_API_URL
    )

    assert b'LOL123' in response.data
    assert b'BAB111' in response.data

# View the first car.
def test_view_first_car(client):
    response = client.get(
        CAR_MANAGEMENT_API_URL + '/1'
    )

    assert b'LOL123'in response.data

# Change the details of the car
def test_change_car_detail(client):
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

# Remove first car.
def test_remove_car(client):
    response = client.get(
        CAR_MANAGEMENT_API_URL + '/1/remove'
    )

    assert b'AHA456' not in response.data