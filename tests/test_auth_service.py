from tests import BaseTestCase
import pytest
import unittest
from app.services import AuthService


class TestAuthService(BaseTestCase):
    auth = AuthService()

    @pytest.mark.auth
    def test_create_token(self):
        token = self.auth.create_token(self.customer_model.id)
        self.assertIsInstance(token, list)
        self.assertEqual(len(token), 2)
        return token

    @pytest.mark.auth
    def test_decode_token(self):
        token = self.auth.create_token(self.customer_model.id)
        access_token, refresh_token = token
        access_payload = self.auth.decode_token(access_token)
        refresh_payload = self.auth.decode_token(refresh_token)
        self.assertIsInstance(access_payload, dict)
        self.assertIsInstance(refresh_payload, dict)
        self.assertEqual(self.customer_model.id, access_payload["id"])
        self.assertEqual("access_token", access_payload["grant_type"])
        self.assertEqual("refresh_token", refresh_payload["grant_type"])
        return access_payload, refresh_payload


if __name__ == "__main__":
    unittest.main()
