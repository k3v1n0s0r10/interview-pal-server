from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import UserModel


class RegisterUserTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-register')
        self.test_user = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """

        response = self.client.post(
            self.register_url, self.test_user, format='json')

        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_register_user_with_missing_fields(self):
        """
        Ensure we can't create a new user with invalid body
        """

        response = self.client.post(self.register_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('username' in response.data)
        self.assertTrue('email' in response.data)
        self.assertTrue('password' in response.data)

    def test_cannot_register_user_with_used_email(self):
        """
        Ensure we can't create a new user with an used email
        """

        response = self.client.post(
            self.register_url, self.test_user, format='json')
        response2 = self.client.post(
            self.register_url, self.test_user, format='json')

        self.assertTrue(UserModel.objects.count() < 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('email' in response2.data)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.test_user = {
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

    def test_login_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """

        response = self.client.post(
            self.url, self.test_user, format='json')

        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
