from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from users.models import Business
from users.views import update_user


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("index")

    def test_index_view_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_index_view_authenticated_user(self):
        user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome Test!")


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpassword",
        )

    def test_login_view_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"), {"email": "test@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_login_view_with_invalid_credentials(self):
        response = self.client.post(
            reverse("login"), {"email": "test@example.com", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials.")


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpassword",
        )

    def test_logout_view_with_authenticated_user(self):
        self.client.login(username="test@example.com", password="testpassword")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LOGGED OUT!")
        self.assertFalse(self.client.session.get("_auth_user_id", None))

    def test_logout_view_with_unauthenticated_user(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_register_view_success(self):
        data = {
            "username": "testuser@example.com",
            "email": "testuser@example.com",
            "password1": "password",
            "password2": "password",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_register_view_passwords_must_match(self):
        data = {
            "username": "testuser@example.com",
            "email": "testuser@example.com",
            "password1": "password1",
            "password2": "password2",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")

    def test_register_view_email_already_exists(self):
        User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        data = {
            "username": "testuser@example.com",
            "email": "testuser@example.com",
            "password1": "password",
            "password2": "password",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already exists.")


class UpdateUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
        )

    # def test_unauthenticated_user_redirected_to_login(self):
    #     """Test that an unauthenticated user is redirected to the login page."""
    #     request = self.factory.get(reverse('update_user'))
    #     response = update_user(request)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('login'))

    def test_authenticated_user_can_view_form(self):
        """Test that an authenticated user can view the update user form."""
        request = self.factory.get(reverse("update_user"))
        request.user = self.user
        response = update_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update Profile")

    def test_authenticated_user_can_update_profile(self):
        """Test that an authenticated user can update their profile."""
        data = {
            "username": "newemail@example.com",
            "email": "newemail@example.com",
            "first_name": "New",
            "last_name": "User",
        }
        request = self.factory.post(reverse("update_user"), data=data)
        request.user = self.user
        # Required to add messages.success() and messages.error() to the request.
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        response = update_user(request)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")

    def test_authenticated_user_cannot_update_profile_with_existing_email(self):
        """Test that an authenticated user cannot update their profile
        with an existing email."""
        User.objects.create_user(
            username="otheruser@example.com",
            email="otheruser@example.com",
            password="password",
        )
        data = {
            "username": "otheruser@example.com",
            "email": "otheruser@example.com",
            "first_name": "New",
            "last_name": "User",
        }
        request = self.factory.post(reverse("update_user"), data=data)
        request.user = self.user
        # Required to add messages.success() and messages.error() to the request.
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        response = update_user(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already exists.")
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, "otheruser@example.com")


class UpdatePasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_user_not_authenticated(self):
        response = self.client.get(reverse("update_password"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/users/login/")

    def test_passwords_must_match(self):
        self.client.force_login(self.user)
        data = {
            "current_password": "testpass123",
            "password1": "newpassword",
            "password2": "differentpassword",
        }
        response = self.client.post(reverse("update_password"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")

    def test_wrong_password(self):
        self.client.force_login(self.user)
        data = {
            "current_password": "wrongpassword",
            "password1": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post(reverse("update_password"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrong password")

    def test_update_password_successfully(self):
        self.client.force_login(self.user)
        data = {
            "current_password": "testpass123",
            "password1": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post(reverse("update_password"), data)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Password Updated Successfully")


class AddBusinessViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        self.client.login(username="testuser@example.com", password="password")
        self.url = reverse("add_business")

    def test_add_business_view_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add your business.")

    def test_add_business_view_post_success(self):
        data = {
            "name": "Test Business",
            "address": "123 Main St.",
            "email": "test@example.com",
            "phone": "555-555-1212",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("view_business", args=(1,)))
        self.assertTrue(Business.objects.filter(name="Test Business").exists())

    def test_add_business_view_post_unauthenticated_user(self):
        self.client.logout()
        data = {
            "name": "Test Business",
            "address": "123 Main St.",
            "email": "test@example.com",
            "phone": "555-555-1212",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("login"))
        self.assertFalse(Business.objects.filter(name="Test Business").exists())


class ViewBusinessViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        self.business = Business.objects.create(
            name="Test Business",
            address="123 Main St",
            owner=self.user,
            phone="123-456-7890",
        )
        self.url = reverse("view_business", args=[self.business.id])

    def test_view_business_view_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, "/users/login/")

    def test_view_business_view_authenticated_user(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View your business.")
        self.assertContains(response, "Test Business")
        self.assertContains(response, "123 Main St")
        self.assertContains(response, "123-456-7890")


class ViewAllBusinessesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        self.business1 = Business.objects.create(
            name="Test Business 1",
            address="123 Main St",
            owner=self.user,
            phone="123-456-7890",
        )
        self.business2 = Business.objects.create(
            name="Test Business 2",
            address="456 Maple St",
            owner=self.user,
            phone="555-555-5555",
        )
        self.url = reverse("view_all_businesses")

    def test_view_all_businesses_view(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertContains(response, "123 Main St")
        self.assertContains(response, "Test Business 2")
        self.assertContains(response, "456 Maple St")
