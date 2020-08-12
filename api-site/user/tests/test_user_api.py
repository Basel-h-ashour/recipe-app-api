from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """tests the user api public endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test that creating a valid user is successful"""
        payload = {
            'email': 'test@testing.com',
            'name': 'tester',
            'password': 'testpass123',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertNotIn('password', res.data)
        self.assertTrue(user.check_password(payload['password']))

    def test_create_user_exists(self):
        """tests creating a user that already exists fails"""
        payload = {
            'email': 'test@testing.com',
            'name': 'tester',
            'password': 'testpass123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """tests that a password shorter than 5 characters fail"""
        payload = {
            'email': 'test@testing.com',
            'name': 'tester',
            'password': 'pass',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            get_user_model().objects.filter(email=payload['email']).exists()
            )

    def test_create_token_for_user(self):
        """tests that a token is created for the user successfully"""
        payload = {
            'email': 'test@testing.com',
            'name': 'tester',
            'password': 'testpass123',
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """tests posting invalid credentials to token"""
        payload = {
            'email': 'test@testing.com',
            'name': 'tester',
            'password': 'testpass123',
        }

        create_user(
            email="test1@testing.com",
            password='testpass123',
            name='tester'
            )

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
