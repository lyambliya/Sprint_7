import pytest
import allure


@allure.feature("Создание курьера")
class TestCourierCreation:
    
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, api_client, random_login, random_password, random_first_name):
        payload = {
            "login": random_login,
            "password": random_password,
            "firstName": random_first_name
        }
        
        response = api_client.create_courier(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
    
    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, api_client, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
            "firstName": registered_courier["firstName"]
        }
        
        response = api_client.create_courier(payload)
        
        assert response.status_code == 409
    
    @allure.title("Создание курьера без логина возвращает ошибку")
    def test_create_courier_without_login(self, api_client, random_password, random_first_name):
        payload = {
            "password": random_password,
            "firstName": random_first_name
        }
        
        response = api_client.create_courier(payload)
        
        assert response.status_code == 400
    
    @allure.title("Создание курьера без пароля возвращает ошибку")
    def test_create_courier_without_password(self, api_client, random_login, random_first_name):
        payload = {
            "login": random_login,
            "firstName": random_first_name
        }
        
        response = api_client.create_courier(payload)
        
        assert response.status_code == 400
    
    @allure.title("Создание курьера без имени - поле не является обязательным")
    def test_create_courier_without_first_name(self, api_client, random_login, random_password):
        payload = {
            "login": random_login,
            "password": random_password
        }
        
        response = api_client.create_courier(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        login_response = api_client.login_courier({"login": random_login, "password": random_password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            api_client.delete_courier(courier_id)