import pytest
import allure
from ..helpers.data_generator import generate_courier_data, generate_login_data


@allure.feature("Создание курьера")
class TestCourierCreation:
    
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, api_client, cleanup_couriers):
        courier_data = generate_courier_data()
        
        response = api_client.create_courier(courier_data)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = api_client.login_courier(generate_login_data(
            courier_data["login"], courier_data["password"]
        ))
        if login_response.status_code == 200:
            cleanup_couriers.append(login_response.json().get("id"))
    
    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, api_client, registered_courier):
        duplicate_data = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
            "firstName": registered_courier["firstName"]
        }
        
        response = api_client.create_courier(duplicate_data)
        
        assert response.status_code == 409
        response_data = response.json()
        assert "message" in response_data
        assert "логин" in response_data["message"].lower() or "уже" in response_data["message"].lower()
    
    @allure.title("Создание курьера без логина возвращает ошибку")
    def test_create_courier_without_login(self, api_client):
        courier_data = generate_courier_data()
        courier_data.pop("login")
        
        response = api_client.create_courier(courier_data)
        
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data
    
    @allure.title("Создание курьера без пароля возвращает ошибку")
    def test_create_courier_without_password(self, api_client):
        courier_data = generate_courier_data()
        courier_data.pop("password")
        
        response = api_client.create_courier(courier_data)
        
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data
    
    @allure.title("Создание курьера без имени - поле не является обязательным")
    def test_create_courier_without_first_name(self, api_client, cleanup_couriers):
        courier_data = generate_courier_data()
        courier_data.pop("firstName")
        
        response = api_client.create_courier(courier_data)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = api_client.login_courier(generate_login_data(
            courier_data["login"], courier_data["password"]
        ))
        if login_response.status_code == 200:
            cleanup_couriers.append(login_response.json().get("id"))