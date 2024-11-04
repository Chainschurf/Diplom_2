import requests
import allure
from data import Endpoints, ErrorMessages


@allure.suite("Order Creating Tests")
@allure.title("Test Order Creation")
class TestCreateOrder:

    @allure.title("Test creating order with authorization")
    def test_create_order_authorized(self, config, create_registered_user):
        ingredients_url = f"{config}{Endpoints.INGREDIENTS}"
        ingredients_response = requests.get(ingredients_url)
        ingredients_data = ingredients_response.json()
        valid_ingredient_ids = [ingredient['_id'] for ingredient in ingredients_data['data'][:2]]
        order_url = f"{config}{Endpoints.ORDERS}"
        access_token = create_registered_user['accessToken']
        headers = {"Authorization": access_token}
        order_data = {"ingredients": valid_ingredient_ids}

        response = requests.post(order_url, json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response_data['success'], "Order creation should be successful"
        assert "order" in response_data, "Response should contain order information"

    @allure.title("Test creating order without authorization")
    def test_create_order_unauthorized(self, config):
        ingredients_url = f"{config}{Endpoints.INGREDIENTS}"
        ingredients_response = requests.get(ingredients_url)
        ingredients_data = ingredients_response.json()
        valid_ingredient_ids = [ingredient['_id'] for ingredient in ingredients_data['data'][:2]]
        order_url = f"{config}{Endpoints.ORDERS}"
        order_data = {"ingredients": valid_ingredient_ids}

        response = requests.post(order_url, json=order_data)
        response_data = response.json()

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response_data['success'], "Order creation should be successful"
        assert "order" in response_data, "Response should contain order information"
        # Наставник сказал прописывать полученный результат как ожидаемый, раз в требованиях иного не сказано.
        # Хотя я бы тут поставил ошибку 401 с сообщением "You should be authorised", по логике.

    @allure.title("Test creating order with ingredients")
    def test_create_order_authorized_with_ingredients(self, config, create_registered_user):
        ingredients_url = f"{config}{Endpoints.INGREDIENTS}"
        ingredients_response = requests.get(ingredients_url)
        ingredients_data = ingredients_response.json()
        valid_ingredient_ids = [ingredient['_id'] for ingredient in ingredients_data['data'][:2]]
        order_url = f"{config}{Endpoints.ORDERS}"
        access_token = create_registered_user['accessToken']
        headers = {"Authorization": access_token}
        order_data = {"ingredients": valid_ingredient_ids}

        response = requests.post(order_url, json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert response_data['success'], "Order creation should be successful"
        assert "order" in response_data, "Response should contain order information"

    @allure.title("Test creating order with missing ingredients")
    def test_create_order_without_ingredients(self, config, create_registered_user):
        order_url = f"{config}{Endpoints.ORDERS}"
        access_token = create_registered_user['accessToken']
        headers = {"Authorization": access_token}
        order_data = {"ingredients": []}

        response = requests.post(order_url, json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
        assert response_data['message'] == ErrorMessages.MISSING_INGREDIENT_IDS, \
            "Expected error message for missing ingredients"

    @allure.title("Test creating order with invalid ingredient hash")
    def test_create_order_invalid_ingredient_hash(self, config, create_registered_user):
        order_url = f"{config}{Endpoints.ORDERS}"
        access_token = create_registered_user['accessToken']
        headers = {"Authorization": access_token}
        order_data = {"ingredients": ["invalid_hash_value"]}

        response = requests.post(order_url, json=order_data, headers=headers)

        assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"
        print(f"Test 'test_create_order_authorized_invalid_ingredient_hash': Response Body (HTML): {response.text}")


