import allure


@allure.feature("Список заказов")
class TestOrdersList:
    
    @allure.title("В теле ответа возвращается список заказов")
    def test_get_orders_list(self, api_client):
        response = api_client.get_orders_list()
        
        assert response.status_code == 200
        response_data = response.json()
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)