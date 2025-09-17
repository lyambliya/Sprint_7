import requests
from .urls import URLs


class APIClient:
    def create_courier(self, data):
        return requests.post(URLs.create_courier(), json=data)
    
    def login_courier(self, data):
        return requests.post(URLs.login_courier(), json=data)
    
    def delete_courier(self, courier_id):
        return requests.delete(URLs.delete_courier(courier_id))
    
    def create_order(self, data):
        return requests.post(URLs.create_order(), json=data)
    
    def get_orders_list(self):
        return requests.get(URLs.get_orders_list())