import requests
import allure
from data import Endpoints


@allure.suite("Order Retrieving Tests")
@allure.title("Test Get User Orders")
class TestGetUserOrders:

    @allure.step("Test retrieving order list for an authorized user")
    def test_get_orders_authorized(self, config, create_registered_user):
        orders_url = f"{config}{Endpoints.ORDERS}"
        access_token = create_registered_user['accessToken']
        if not access_token.startswith("Bearer "):
            access_token = f"Bearer {access_token}"

        headers = {
            "Authorization": access_token
        }

        response = requests.get(orders_url, headers=headers)
        response_data = response.json()

        assert response.status_code == 200, f"Expected status code 200 for successful order retrieval, but got {response.status_code}"
        assert response_data['success'], "Order retrieval should be successful"
        assert "orders" in response_data, "Response should contain the 'orders' field"
        assert isinstance(response_data['orders'], list), "Expected 'orders' to be a list"

    @allure.step("Test retrieving order list for an unauthorized user")
    def test_get_orders_unauthorized(self, config):
        orders_url = f"{config}{Endpoints.ORDERS}"

        response = requests.get(orders_url)
        response_data = response.json()

        assert response.status_code == 401, f"Expected status code 401 for unauthorized order retrieval, but got {response.status_code}"
        assert response_data['message'] == "You should be authorised", "Expected error message for unauthorized access"
