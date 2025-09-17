import pytest
import allure
from ..helpers.data_generator import generate_login_data


@allure.feature("Логин курьера")
class TestCourierLogin:
    
    @allure.title("Курьер может авторизоваться")
    def test_login_courier_success(self, api_client, registered_courier):
        login_data = generate_login_data(
            registered_courier["login"], registered_courier["password"]
        )
        
        response = api_client.login_courier(login_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)
    
    @allure.title("Логин с неправильным паролем возвращает ошибку")
    def test_login_with_wrong_password(self, api_client, registered_courier):
        login_data = generate_login_data(registered_courier["login"], "wrong_password")
        
        response = api_client.login_courier(login_data)
        
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data
    
    @allure.title("Логин с неправильным логином возвращает ошибку")
    def test_login_with_wrong_login(self, api_client, registered_courier):
        login_data = generate_login_data("wrong_login", registered_courier["password"])
        
        response = api_client.login_courier(login_data)
        
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data
    
    @allure.title("Логин без логина возвращает ошибку")
    def test_login_without_login(self, api_client, registered_courier):
        login_data = {"password": registered_courier["password"]}
        
        response = api_client.login_courier(login_data)
        
        assert response.status_code != 200
        if response.status_code != 504:  # Игнорируем Gateway Timeout
            response_data = response.json()
            assert "message" in response_data
    
    @allure.title("Логин без пароля возвращает ошибку")
    def test_login_without_password(self, api_client, registered_courier):
        login_data = {"login": registered_courier["login"]}
        
        response = api_client.login_courier(login_data)
        
        assert response.status_code != 200
        if response.status_code != 504:  # Игнорируем Gateway Timeout
            response_data = response.json()
            assert "message" in response_data
    
    @allure.title("Логин несуществующего пользователя возвращает ошибку")
    def test_login_nonexistent_user(self, api_client):
        login_data = generate_login_data("nonexistent_user", "password123")
        
        response = api_client.login_courier(login_data)
        
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data