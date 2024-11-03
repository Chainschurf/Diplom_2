import requests
import allure
from data import Endpoints


@allure.suite("User Login Tests")
@allure.title("Test User Login")
class TestUserLogin:

    @allure.step("Test successful login for an existing user")
    def test_login_successfully(self, config, create_registered_user):
        url = f"{config}{Endpoints.LOGIN}"
        user_data = {
            "email": create_registered_user['user_data']['email'],
            "password": create_registered_user['user_data']['password']
        }

        response = requests.post(url, json=user_data)

        assert response.status_code == 200, "Expected status code 200 for successful login"
        response_data = response.json()
        assert response_data['success'], "Login should be successful"
        assert "accessToken" in response_data, "Response should contain accessToken"
        assert "refreshToken" in response_data, "Response should contain refreshToken"

    @allure.step("Test login with incorrect credentials")
    def test_login_with_incorrect_credentials(self, config):
        url = f"{config}{Endpoints.LOGIN}"
        user_data = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }

        response = requests.post(url, json=user_data)
        response_data = response.json()

        assert response.status_code == 401, "Expected status code 401 for incorrect credentials"
        assert response_data['message'] == "email or password are incorrect", \
            "Expected error message for incorrect credentials"
