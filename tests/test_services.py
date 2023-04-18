from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.services.models import Business


class AddBusinessViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )

    def test_add_view(self):
        self.client.login(username="testuser@example.com", password="testpass")

        response = self.client.get(reverse("add_business"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account-add-business")
        self.assertTemplateUsed(response, "services/add_business.html")

        data = {
            "name": "Test Business",
            "address": "123 Test St",
            "email": "test@example.com",
            "phone": "123-456-7890",
        }
        response = self.client.post(reverse("add_business"), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/business/{}/".format(Business.objects.first().id)
        )
        self.assertEqual(Business.objects.count(), 1)
        self.assertEqual(Business.objects.first().name, "Test Business")
        self.assertEqual(Business.objects.first().address, "123 Test St")
        self.assertEqual(Business.objects.first().email, "test@example.com")
        self.assertEqual(Business.objects.first().phone, "123-456-7890")
        self.assertEqual(Business.objects.first().owner, self.user)

    def test_add_view_requires_login(self):
        response = self.client.get(reverse("add_business"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/business/add/")


class ViewBusinessViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1@example.com",
            email="testuser1@example.com",
            password="testpass1",
        )
        self.user2 = User.objects.create_user(
            username="testuser2@example.com",
            email="testuser2@example.com",
            password="testpass2",
        )
        self.business1 = Business.objects.create(
            name="Test Business 1",
            address="123 Test St",
            email="test1@example.com",
            phone="123-456-7890",
            owner=self.user1,
        )
        self.business2 = Business.objects.create(
            name="Test Business 2",
            address="456 Test St",
            email="test2@example.com",
            phone="123-456-7890",
            owner=self.user2,
        )

    def test_view_view(self):
        self.client.login(username="testuser1@example.com", password="testpass1")
        response = self.client.get(reverse("view_business", args=(self.business1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertNotContains(response, "Test Business 2")
        self.assertTemplateUsed(response, "services/view_business.html")

    def test_view_view_requires_login(self):
        response = self.client.get(reverse("view_business", args=(self.business1.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/business/{}/".format(self.business1.id),
        )


class ServicesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
        )
        self.business1 = Business.objects.create(
            name="Test Business 1",
            email="test1@example.com",
            phone="123-456-7890",
            address="123 Test St",
            owner=self.user,
        )
        self.business2 = Business.objects.create(
            name="Test Business 2",
            email="test2@example.com",
            phone="123-456-7890",
            address="456 Test St",
            owner=self.user,
        )

    def test_services_view(self):
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertContains(response, "Test Business 2")
        self.assertTemplateUsed(response, "services/services.html")

    def test_services_view_authenticated_user(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertContains(response, "Test Business 2")
        self.assertTemplateUsed(response, "services/services.html")

    def test_services_view_no_businesses(self):
        Business.objects.all().delete()
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/services.html")


class BusinessesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1@example.com",
            email="testuser1@example.com",
            password="testpass1",
        )
        self.user2 = User.objects.create_user(
            username="testuser2@example.com",
            email="testuser2@example.com",
            password="testpass2",
        )
        self.business1 = Business.objects.create(
            name="Test Business 1",
            email="test1@example.com",
            phone="123-456-7890",
            address="123 Test St",
            owner=self.user1,
        )
        self.business2 = Business.objects.create(
            name="Test Business 2",
            email="test2@example.com",
            phone="123-456-7890",
            address="456 Test St",
            owner=self.user2,
        )

    def test_businesses_view(self):
        self.client.login(username="testuser1@example.com", password="testpass1")
        response = self.client.get(reverse("user_businesses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertNotContains(response, "Test Business 2")
        self.assertTemplateUsed(response, "services/businesses.html")

    def test_businesses_view_requires_login(self):
        response = self.client.get(reverse("user_businesses"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/business/")

    def test_businesses_view_no_businesses(self):
        self.client.login(username="testuser2@example.com", password="testpass2")
        response = self.client.get(reverse("user_businesses"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/businesses.html")
