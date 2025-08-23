from datetime import timedelta
from .utils import *
from fastapi import status, HTTPException
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM,get_current_user
from jose import jwt 
import pytest

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    not_existed_user = authenticate_user('wrongusername', 'testpassword', db)
    assert not_existed_user is False

    wrong_pass_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_pass_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature' : False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def get_current_user_valid_token():
    encode = {'sub': 'user', 'id': 1, 'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username' : 'user', 'user_id': 1, 'user_role': 'user'}


@pytest.mark.asyncio
async def get_current_user_invalid():
    encode = {'role':'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user'
