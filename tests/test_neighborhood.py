from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from neighborhood.models import Neighborhood


class NeighborhoodsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Neighborhood.objects.create(
            name="Test Neighborhood",
            borough="Test Borough",
            description="Test description",
            lat=40.7128,
            lon=-74.0060,
        )

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )

    def test_neighborhoods_view(self):
        response = self.client.get(reverse("neighborhoods"))

        self.assertEqual(response.status_code, 200)

        self.assertIn("neighborhoods", response.context)
        neighborhoods = response.context["neighborhoods"]
        self.assertEqual(neighborhoods.count(), 1)

    def test_neighborhood_view(self):
        neighborhood = Neighborhood.objects.first()
        response = self.client.get(reverse("neighborhood", args=[neighborhood.pk]))

        self.assertEqual(response.status_code, 200)

        self.assertIn("neighborhood", response.context)
        self.assertEqual(response.context["neighborhood"], neighborhood)

    def test_borough_view(self):
        response = self.client.get(reverse("borough", args=["Test Borough"]))

        self.assertEqual(response.status_code, 200)

        self.assertIn("borough", response.context)
        self.assertIn("neighborhoods", response.context)
        borough = response.context["borough"]
        neighborhoods = response.context["neighborhoods"]
        self.assertEqual(borough, "Test Borough")
        self.assertEqual(neighborhoods.count(), 1)

    def test_authenticated_user_view(self):
        self.client.login(username="testuser@example.com", password="password")

        response = self.client.get(reverse("neighborhoods"))
        self.assertEqual(response.status_code, 200)

        neighborhood = Neighborhood.objects.first()
        response = self.client.get(reverse("neighborhood", args=[neighborhood.pk]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("borough", args=["Test Borough"]))
        self.assertEqual(response.status_code, 200)

        self.assertIn("firstname", response.context)
        self.assertIsNotNone(response.context["firstname"])
