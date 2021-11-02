from tests import BaseTestCase
from app.models import CustomerModel
import unittest
import pytest


class TestModels(BaseTestCase):
    @pytest.mark.model
    def test_customer_model(self):
        self.assertEqual(CustomerModel.query.count(), 1)
        self.assertTrue(CustomerModel.query.get(1))
        self.assertEqual(self.customer_model, CustomerModel.query.get(1))
        for key in self.customer.keys():
            self.assertEqual(getattr(self.customer_model, key),
                             getattr(CustomerModel.query.get(1), key))


if __name__ == "__main__":
    unittest.main()
