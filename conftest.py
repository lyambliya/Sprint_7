import pytest
import requests
from .api.client import APIClient
from .api.urls import URLs
from .helpers.data_generator import generate_courier_data


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def registered_courier():
    courier_data = generate_courier_data()
    
    response = requests.post(URLs.create_courier(), json=courier_data)
    if response.status_code != 201:
        pytest.fail("Failed to register courier for test")
    
    login_data = {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }
    
    login_response = requests.post(URLs.login_courier(), json=login_data)
    if login_response.status_code == 200:
        courier_data["id"] = login_response.json().get("id")
    else:
        pytest.fail("Failed to login courier for test")
    
    yield courier_data
    
    if courier_data.get("id"):
        try:
            APIClient().delete_courier(courier_data["id"])
        except:
            pass


@pytest.fixture
def cleanup_couriers():
    created_couriers = []
    yield created_couriers
    
    for courier_id in created_couriers:
        try:
            APIClient().delete_courier(courier_id)
        except:
            pass