import requests
import allure
from data import Endpoints
from helpers import get_sign_up_data


@allure.suite("User Updating Tests")
@allure.title("Test Update User")
class TestUpdateUser:

    @allure.step("Test updating user data with authorization")
    def test_update_user_authorized(self, config, create_registered_user):
        user_url = f"{config}{Endpoints.USER}"
        access_token = create_registered_user['accessToken']
        if not access_token.startswith("Bearer "):
            access_token = f"Bearer {access_token}"
        headers = {
            "Authorization": access_token
        }
        name, email, password = get_sign_up_data()
        updated_data = {
            "name": name,
            "email": email
        }

        response = requests.patch(user_url, json=updated_data, headers=headers)
        response_data = response.json()

        assert response.status_code == 200, f"Expected status code 200 for successful update, but got {response.status_code}"
        assert response_data['success'], "User update should be successful"
        assert response_data['user']['name'] == updated_data['name'], "User name should be updated"
        assert response_data['user']['email'] == updated_data['email'], "User email should be updated"

    @allure.step("Test updating user data without authorization")
    def test_update_user_unauthorized(self, config):
        user_url = f"{config}{Endpoints.USER}"
        updated_data = {
            "name": "Unauthorized Name"
        }

        response = requests.patch(user_url, json=updated_data)
        response_data = response.json()

        assert response.status_code == 401, f"Expected status code 401 for unauthorized update, but got {response.status_code}"
        assert response_data['message'] == "You should be authorised", "Expected error message for unauthorized access"

