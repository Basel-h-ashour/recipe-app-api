from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests models in the core app"""

    def test_create_user_with_email(self):
        """tests create_user function works using an email"""
        name = "Tester"
        email = "test@tester.com"
        password = "testpass"

        user = get_user_model().objects.create_user(
            email=email,
            name=name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """tests a new user email is normalized"""
        email = "test@TESTER.COM"
        user = get_user_model().objects.create_user(
            email=email,
            name="any",
            password="any"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """tests creating user without an email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                name="any",
                password="any"
            )

    def test_create_superuser(self):
        """tests creating a new superuser"""
        name = "Tester"
        email = "test@tester.com"
        password = "testpass"

        user = get_user_model().objects.create_superuser(
            email=email,
            name=name,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
