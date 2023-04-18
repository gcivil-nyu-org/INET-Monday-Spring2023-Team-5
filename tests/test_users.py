from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserAccountViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_user_account_view(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("user_account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account")
        self.assertTemplateUsed(response, "users/index.html")

    def test_user_account_view_requires_login(self):
        response = self.client.get(reverse("user_account"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?/=/accounts/")


class AccountRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_account_register_view_get(self):
        response = self.client.get(reverse("account_register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "register")
        self.assertTemplateUsed(response, "users/account_register.html")

    def test_account_register_view_post_valid_credentials(self):
        response = self.client.post(
            reverse("account_register"),
            {
                "email": "testuser@example.com",
                "password1": "testpass",
                "password2": "testpass",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/")
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_account_register_view_post_passwords_must_match(self):
        response = self.client.post(
            reverse("account_register"),
            {
                "email": "testuser@example.com",
                "password1": "testpass",
                "password2": "wrongpass",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")
        self.assertTemplateUsed(response, "users/account_register.html")

    def test_account_register_view_post_email_already_exists(self):
        User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )
        response = self.client.post(
            reverse("account_register"),
            {
                "email": "testuser@example.com",
                "password1": "testpass",
                "password2": "testpass",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already exists.")
        self.assertTemplateUsed(response, "users/account_register.html")

    def test_account_register_view_user_already_logged_in(self):
        User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("account_register"),
            {
                "email": "anothertestuser@example.com",
                "password1": "testpass",
                "password2": "testpass",
                "first_name": "Another Test",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 301)


class AccountLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_account_login_view_get(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login")
        self.assertTemplateUsed(response, "users/account_login.html")

    def test_account_login_view_post_valid_credentials(self):
        response = self.client.post(
            reverse("account_login"),
            {
                "username": "testuser@example.com",
                "email": "testuser@example.com",
                "password": "testpass",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/")

    def test_account_login_view_post_invalid_credentials(self):
        response = self.client.post(
            reverse("account_login"),
            {
                "username": "testuser@example.com",
                "email": "testuser@example.com",
                "password": "wrongpass",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials.")
        self.assertTemplateUsed(response, "users/account_login.html")

    def test_account_login_view_user_already_logged_in(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("account_login"),
            {
                "username": "testuser@example.com",
                "email": "testuser@example.com",
                "password": "wrongpass",
            },
        )
        self.assertEqual(response.status_code, 301)


class AccountLogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_account_logout_view(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have been logged out.")
        self.assertTemplateUsed(response, "users/account_logout.html")
        self.assertFalse("_auth_user_id" in self.client.session)


class AccountDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_account_delete_view_get(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("account_delete"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account-delete")
        self.assertTemplateUsed(response, "users/account_delete.html")

    def test_account_delete_view_post_valid_password(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(reverse("account_delete"), {"password": "testpass"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/register/")
        self.assertFalse(User.objects.filter(email="testuser@example.com").exists())

    def test_account_delete_view_post_invalid_password(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("account_delete"), {"password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrong password")
        self.assertTemplateUsed(response, "users/account_delete.html")
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())


class UpdateAccountViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_update_account_view_get(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("update_account"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account-edit")
        self.assertTemplateUsed(response, "users/update_account.html")

    def test_update_account_view_post_valid_data(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("update_account"),
            {
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_account"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newuser@example.com")
        self.assertEqual(self.user.email, "newuser@example.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")

    def test_update_account_view_post_invalid_email(self):
        User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="otherpass",
        )
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("update_account"),
            {
                "email": "otheruser@example.com",
                "first_name": "New",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update_account.html")
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "testuser@example.com")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")


class UpdatePasswordViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_update_password_view_get(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("update_password"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account-update-password")
        self.assertTemplateUsed(response, "users/update_password.html")

    def test_update_password_view_post_valid_data(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("update_password"),
            {
                "current_password": "testpass",
                "password1": "newpass",
                "password2": "newpass",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_account"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass"))

    def test_update_password_view_post_invalid_password(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("update_password"),
            {
                "current_password": "wrongpass",
                "password1": "newpass",
                "password2": "newpass",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update_password.html")
        self.assertTrue(self.user.check_password("testpass"))

    def test_update_password_view_post_mismatched_passwords(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("update_password"),
            {
                "current_password": "testpass",
                "password1": "newpass",
                "password2": "wrongpass",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update_password.html")
        self.assertTrue(self.user.check_password("testpass"))
