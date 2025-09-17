import pytest
import requests
from .api.client import APIClient
from .api.urls import URLs
from .helpers.data_generator import generate_courier_data, generate_order_data


def register_new_courier():
    courier_data = generate_courier_data()
    
    response = requests.post(URLs.create_courier(), json=courier_data)
    
    if response.status_code == 201:
        return courier_data
    return None


def register_and_login_courier():
    courier_data = register_new_courier()
    if not courier_data:
        return None
    
    login_data = {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }
    
    response = requests.post(URLs.login_courier(), json=login_data)
    
    if response.status_code == 200:
        courier_data["id"] = response.json().get("id")
        return courier_data
    
    return None


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
    return generate_order_data()


@pytest.fixture
def cleanup_couriers():
    created_couriers = []
    yield created_couriers
    
    for courier_id in created_couriers:
        try:
            APIClient().delete_courier(courier_id)
        except:
            pass