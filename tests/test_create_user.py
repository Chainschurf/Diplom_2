import pytest
import requests
import allure
from data import Endpoints, ErrorMessages


@allure.suite("User Creation Tests")
@allure.title("Test Create User")
class TestCreateUser:

    @allure.title("Test successfully creating a unique user")
    def test_create_unique_user(self, create_registered_user):
        user_data = create_registered_user['user_data']
        access_token = create_registered_user['accessToken']
        status_code = create_registered_user['status_code']

        assert status_code == 200, f"Expected status code 200 for successful registration, but got {status_code}"
        assert access_token is not None, "Expected accessToken for successful registration"
        assert user_data['email'] is not None, "Email should be present in the user data"
        assert user_data['name'] is not None, "Name should be present in the user data"

    @allure.title("Test creating an already registered user")
    def test_create_existing_user(self, config, create_registered_user):
        url = f"{config}{Endpoints.REGISTER}"
        user_data = create_registered_user['user_data']

        response = requests.post(url, json=user_data)

        assert response.status_code == 403, "Expected status code 403 for already registered user"
        response_data = response.json()
        assert response_data['message'] == ErrorMessages.USER_ALREADY_EXISTS, "Expected 'User already exists' message"

    @allure.title("Test creating user without required field")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, config, missing_field, create_registered_user):
        url = f"{config}{Endpoints.REGISTER}"
        user_data = create_registered_user['user_data']
        del user_data[missing_field]

        response = requests.post(url, json=user_data)

        assert response.status_code == 403, "Expected status code 403 for missing required field"
        response_data = response.json()
        assert response_data['message'] == ErrorMessages.MISSING_REQUIRED_FIELDS, \
            "Expected error message for missing required fields"
