from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(name='Tester',
                email='test@londonappdev.com', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        email=email,
        name=name,
        password=password
        )


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
