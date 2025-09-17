import requests
from .data_generator import generate_courier_data
from api.urls import URLs


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


def login_courier_and_get_id(api_client, login, password):
    login_data = {
        "login": login,
        "password": password
    }
    
    response = api_client.login_courier(login_data)
    if response.status_code == 200:
        return response.json().get("id")
    return None