import pytest
from io import BytesIO
from http import HTTPStatus
from MasterCSS.tests.test_fixture import client

# Route renders register.html when not logged in
def test_render_register(client):
    response = client.get('/register')
    assert b'Register' in response.data

# Route renders login.html when not logged in
def test_render_login(client):
    response = client.get('/login')
    assert b'Login' in response.data

# Route renders index.html when not logged in
def test_render_index(client):
    response = client.get('/')
    assert b'Welcome to Car Share System!' in response.data

# Route to route that doesn't exist, renders the 404 template.
def test_404_not_found(client):
    response = client.get('/asdfadfasdf')
    assert b'404 Not Found' in response.data
    assert response.status_code == HTTPStatus.NOT_FOUND

# Test unauthorised access to auth-secured pages when not logged in
def test_unauthorised(client):
    response = client.get('/myinfo')
    assert b'Unauthorised' in response.data
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = client.get('/mybookings')
    assert b'Unauthorised' in response.data
    assert response.status_code == HTTPStatus.UNAUTHORIZED

# Test register with invalid values
def test_register_invalid(client):
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
    response = client.get('/logout', follow_redirects=True)
    assert b'Welcome to Car Share System!' in response.data

# Test login with unregistered user
def test_login_unregistered(client):
    response = client.post(
        '/login',
        data=dict(
            username="example1",
            password="password1"
        ),
        follow_redirects=True
    )
    assert b'User not found!' in response.data

# Test login with invalid password
def test_login_invalid(client):
    response = client.post(
        '/login',
        data=dict(
            username="example",
            password="password1"
        ),
        follow_redirects=True
    )
    assert b'Password mismatch!' in response.data

# Test login with registered user
def test_login_valid(client):
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

# Test dashboard route after logged in
def test_dashboard_route(client):
    response = client.get(
        '/'
    )

    assert b'Let\'s book you a car!' in response.data