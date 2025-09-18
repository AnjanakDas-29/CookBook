from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile, Recipe


class UserTests(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            role="user"
        )
        self.admin = UserProfile.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )

    def test_user_registration(self):
        url = reverse("user-register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
            "role": "user"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 3)

    def test_user_login(self):
        url = reverse("token_obtain_pair")
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_logout(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged out")

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("user-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_cannot_list_users(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RecipeTests(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="recipeuser",
            email="recipe@example.com",
            password="password123",
            role="user"
        )
        self.admin = UserProfile.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_recipe_authenticated(self):
        self.authenticate(self.user)
        url = reverse("List-Create")
        data = {
            "title": "My Recipe",
            "description": "Delicious food",
            "ingredients": "Rice, Curry",
            "instructions": "Cook well"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_create_recipe_unauthenticated(self):
        url = reverse("List-Create")
        data = {
            "title": "Fail Recipe",
            "description": "No auth",
            "ingredients": "Nothing",
            "instructions": "Do nothing"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_recipes(self):
        Recipe.objects.create(
            title="Test Recipe",
            ingredients="Eggs",
            instructions="Boil",
            created_by=self.user
        )
        url = reverse("List-Create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_retrieve_recipe(self):
        recipe = Recipe.objects.create(
            title="Retrieve Recipe",
            ingredients="Fish",
            instructions="Fry",
            created_by=self.user
        )
        self.authenticate(self.user)
        url = reverse("retrieve-update-delete", args=[recipe.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Retrieve Recipe")
    def test_update_recipe_owner(self):
        recipe = Recipe.objects.create(
            title="Old Title",
            ingredients="Veg",
            instructions="Cook",
            created_by=self.user
        )
        self.authenticate(self.user)
        url = reverse("retrieve-update-delete", args=[recipe.id])
        response = self.client.patch(url, {"title": "New Title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, "New Title")

    def test_update_recipe_non_owner_forbidden(self):
        other_user = UserProfile.objects.create_user(
            username="other",
            email="other@example.com",
            password="password123"
        )
        recipe = Recipe.objects.create(
            title="Other Recipe",
            ingredients="Milk",
            instructions="Boil",
            created_by=other_user
        )
        self.authenticate(self.user)
        url = reverse("retrieve-update-delete", args=[recipe.id])
        response = self.client.patch(url, {"title": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_recipe_owner(self):
        recipe = Recipe.objects.create(
            title="Delete Me",
            ingredients="Wheat",
            instructions="Bake",
            created_by=self.user
        )
        self.authenticate(self.user)
        url = reverse("retrieve-update-delete", args=[recipe.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Recipe deleted Successfully")

    def test_my_recipes_user(self):
        Recipe.objects.create(
            title="User Recipe",
            ingredients="Oil",
            instructions="Heat",
            created_by=self.user
        )
        self.authenticate(self.user)
        url = reverse("myrecipies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_my_recipes_admin_gets_all(self):
        Recipe.objects.create(
            title="Admin Recipe",
            ingredients="Sugar",
            instructions="Mix",
            created_by=self.user
        )
        self.authenticate(self.admin)
        url = reverse("myrecipies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
