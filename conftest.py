import pytest
import requests
import random
import string


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def register_new_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', json=payload)
    
    if response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name, "id": None}
    return None


def register_and_login_courier():
    courier_data = register_new_courier()
    if not courier_data:
        return None
    
    login_payload = {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }
    
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', json=login_payload)
    
    if response.status_code == 200:
        courier_data["id"] = response.json().get("id")
        return courier_data
    
    return None


class APIClient:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    def create_courier(self, data):
        return requests.post(f"{self.BASE_URL}/api/v1/courier", json=data)
    
    def login_courier(self, data):
        return requests.post(f"{self.BASE_URL}/api/v1/courier/login", json=data)
    
    def delete_courier(self, courier_id):
        return requests.delete(f"{self.BASE_URL}/api/v1/courier/{courier_id}")
    
    def create_order(self, data):
        return requests.post(f"{self.BASE_URL}/api/v1/orders", json=data)
    
    def get_orders_list(self):
        return requests.get(f"{self.BASE_URL}/api/v1/orders")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def registered_courier():
    courier = register_and_login_courier()
    yield courier
    
    if courier and courier.get("id"):
        try:
            APIClient().delete_courier(courier["id"])
        except:
            pass


@pytest.fixture
def order_data():
    return {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Пушкина, д. 10",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 5,
        "deliveryDate": "2024-12-31",
        "comment": "Тестовый заказ"
    }


@pytest.fixture
def random_login():
    return generate_random_string(10)


@pytest.fixture
def random_password():
    return generate_random_string(10)


@pytest.fixture
def random_first_name():
    return generate_random_string(10)