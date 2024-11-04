import pytest
import requests
from helpers import get_sign_up_data
from data import Config, Endpoints


@pytest.fixture
def config():
    return Config.BASE_URL


@pytest.fixture
def create_registered_user():
    url = f"{Config.BASE_URL}{Endpoints.REGISTER}"
    name, email, password = get_sign_up_data()
    user_data = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(url, json=user_data)
    response_data = response.json()
    access_token = response_data.get("accessToken")

    if not access_token:
        raise ValueError(f"User registration failed, no accessToken returned. Response: {response.text}")

    yield {
        "user_data": user_data,
        "accessToken": access_token,
        "status_code": response.status_code
    }

    delete_url = f"{Config.BASE_URL}{Endpoints.USER}"
    headers = {"Authorization": access_token}
    requests.delete(delete_url, headers=headers)

