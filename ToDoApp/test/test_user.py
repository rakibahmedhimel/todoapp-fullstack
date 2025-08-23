from .utils import *
from fastapi import status
from ..routers.user import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == 200
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['first_name'] == test_user.first_name
    assert response.json()['last_name'] == test_user.last_name
    assert response.json()['hashed_password'] == test_user.hashed_password
    assert response.json()['role'] == test_user.role
    assert response.json()['phone_number'] == test_user.phone_number

def test_change_password_success(test_user):
    response = client.put('/user/password', json={'password' : 'testpassword', 'new_password' : 'new_password'})
    assert response.status_code == 204


def test_change_password_failed(test_user):
    response = client.put('/user/password', json={'password' : 'wrong_password', 'new_password' : 'new_password'})
    assert response.status_code == 401
    assert response.json() == {'detail' : 'Wrong Password'}

def test_change_phone_number(test_user):
    response = client.put('/user/phone/021454478')
    assert response.status_code == 204