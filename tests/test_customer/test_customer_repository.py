from app.repositories import CustomerRepository
from tests import BaseTestCase
import pytest
from app.models import CustomerModel
import unittest

NEW_DATA = {
    "name": "new_name",
    "username": "new_username",
    "email": "new_email",
    "password": "new_password"
}


class TestCustomerRepository(BaseTestCase):
    @pytest.mark.customer
    def test_index(self):
        get_all_customers = CustomerRepository(self.redis).index()
        self.assertEqual(CustomerModel.query.count(), 1)
        self.assertIsInstance(get_all_customers, list)
        self.assertEqual(len(get_all_customers), 1)
        self.assertIsInstance(get_all_customers[0], CustomerModel)
        self.assertEqual(get_all_customers[0].id, 1)
        self.assertEqual(self.customer_model.name, get_all_customers[0].name)
        self.assertEqual(self.customer_model.email, get_all_customers[0].email)
        self.assertEqual(self.customer_model.username, get_all_customers[0].username)
        self.assertEqual(self.customer_model.password, get_all_customers[0].password)

    @pytest.mark.customer
    def test_create(self):
        create_new_data = CustomerRepository(self.redis).create(NEW_DATA)
        self.assertEqual(CustomerModel.query.count(), 2)
        self.assertIsInstance(create_new_data, CustomerModel)
        self.assertEqual(create_new_data.id, 2)
        self.assertEqual(NEW_DATA["name"], create_new_data.name)
        self.assertEqual(NEW_DATA["email"], create_new_data.email)
        self.assertEqual(NEW_DATA["username"], create_new_data.username)
        self.assertTrue(
            create_new_data.verify_password(NEW_DATA["password"]))


if __name__ == "__main__":
    unittest.main()
