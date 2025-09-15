import pytest
import allure


@allure.feature("Логин курьера")
class TestCourierLogin:
    
    @allure.title("Курьер может авторизоваться")
    def test_login_courier_success(self, api_client, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"]
        }
        
        response = api_client.login_courier(payload)
        
        assert response.status_code == 200
        assert "id" in response.json()
    
    @allure.title("Логин с неправильным паролем возвращает ошибку")
    def test_login_with_wrong_password(self, api_client, registered_courier):
        payload = {
            "login": registered_courier["login"],
            "password": "wrong_password"
        }
        
        response = api_client.login_courier(payload)
        
        assert response.status_code == 404
    
    @allure.title("Логин с неправильным логином возвращает ошибку")
    def test_login_with_wrong_login(self, api_client, registered_courier):
        payload = {
            "login": "wrong_login",
            "password": registered_courier["password"]
        }
        
        response = api_client.login_courier(payload)
        
        assert response.status_code == 404
    
    @allure.title("Логин без логина возвращает ошибку")
    def test_login_without_login(self, api_client, registered_courier):
        payload = {
            "password": registered_courier["password"]
        }
        
        response = api_client.login_courier(payload)
        
        assert response.status_code != 200
    
    @allure.title("Логин без пароля возвращает ошибку")
    def test_login_without_password(self, api_client, registered_courier):
        payload = {
            "login": registered_courier["login"]
        }
        
        response = api_client.login_courier(payload)
        
        assert response.status_code != 200
    
    @allure.title("Логин несуществующего пользователя возвращает ошибку")
    def test_login_nonexistent_user(self, api_client):
        payload = {
            "login": "nonexistent_user",
            "password": "password123"
        }
        
        response = api_client.login_courier(payload)
        
        assert response.status_code == 404