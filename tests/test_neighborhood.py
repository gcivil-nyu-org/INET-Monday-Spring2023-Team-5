from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )

    def test_index_view_unauthenticated(self):
        response = self.client.get(reverse("neighborhoods"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "neighborhoods/index.html")
        self.assertEqual(response.context["page"], "neighborhoods")
        self.assertNotIn("firstname", response.context)

    def test_index_view_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(reverse("neighborhoods"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "neighborhoods/index.html")
        self.assertEqual(response.context["page"], "neighborhoods")
        self.assertEqual(response.context["firstname"], "Test")
