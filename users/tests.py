from rest_framework import status
from rest_framework.test import APITestCase


class UsersTestCase(APITestCase):

    def test_UserRegistration(self):
        data = {
            "username": "Test",
            "password": "test",
            "password_confirm": "test",
            "telegram_id": 1234567890
        }
        resp = self.client.post('/users/register/', data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
