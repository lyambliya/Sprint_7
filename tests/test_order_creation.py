import pytest
import allure


@allure.feature("Создание заказа")
class TestOrderCreation:
    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    @allure.title("Создание заказа с разными вариантами цветов")
    def test_create_order_with_different_colors(self, api_client, order_data, color):
        if color is not None:
            order_data["color"] = color
        
        response = api_client.create_order(order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()