class URLs:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    
    @staticmethod
    def create_courier():
        return f"{URLs.BASE_URL}/api/v1/courier"
    
    @staticmethod
    def login_courier():
        return f"{URLs.BASE_URL}/api/v1/courier/login"
    
    @staticmethod
    def delete_courier(courier_id):
        return f"{URLs.BASE_URL}/api/v1/courier/{courier_id}"
    
    @staticmethod
    def create_order():
        return f"{URLs.BASE_URL}/api/v1/orders"
    
    @staticmethod
    def get_orders_list():
        return f"{URLs.BASE_URL}/api/v1/orders"