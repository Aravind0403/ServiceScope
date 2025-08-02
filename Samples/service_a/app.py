import requests

def get_customer_data():
    response = requests.get("http://customer-service.internal/api/v1/customers")
    return response.json()

def process_payment():
    response = requests.post("http://localhost:5001/api/pay")
    return response.status_code