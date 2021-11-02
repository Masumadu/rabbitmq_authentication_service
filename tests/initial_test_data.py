from app.models import CustomerModel


def setup_data():
    customer = {
        "name": "test_customer",
        "username": "test_customer_username",
        "email": "test_customer_email",
        "password": "test_customer_password"
    }
    return customer


def model_data():
    customer_data = setup_data()
    customer = CustomerModel(**customer_data)
    return customer
