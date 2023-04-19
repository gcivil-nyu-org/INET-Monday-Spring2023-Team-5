from django.test import TestCase
from django.contrib.auth.models import User

from users.services.models import Business
from users.marketplace.models import Listing
from neighborhood.models import Neighborhood


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
        )
        self.neighborhood = Neighborhood.objects.create(
            name="Test Neighborhood",
            borough="Test Borough",
            description="Test description",
            lat=0,
            lon=0,
        )
        self.business = Business.objects.create(
            name="Test Business",
            address="Test Address",
            owner=self.user,
            neighborhood=self.neighborhood,
            email="test@example.com",
            phone="1234567890",
        )
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="Test description",
            price=100,
            email="test@example.com",
            phone="1234567890",
            address="Test Address",
            owner=self.user,
            neighborhood=self.neighborhood,
        )

    def test_business_model(self):
        business = self.business
        self.assertEqual(str(business), "Test Business")
        self.assertEqual(business.name, "Test Business")
        self.assertEqual(business.address, "Test Address")
        self.assertEqual(business.owner, self.user)
        self.assertEqual(business.neighborhood, self.neighborhood)
        self.assertEqual(business.email, "test@example.com")
        self.assertEqual(business.phone, "1234567890")

    def test_neighborhood_model(self):
        neighborhood = self.neighborhood
        self.assertEqual(str(neighborhood), "Test Neighborhood")
        self.assertEqual(neighborhood.name, "Test Neighborhood")
        self.assertEqual(neighborhood.borough, "Test Borough")
        self.assertEqual(neighborhood.description, "Test description")
        self.assertEqual(neighborhood.lat, 0)
        self.assertEqual(neighborhood.lon, 0)
        self.assertEqual(neighborhood.get_geopoint(), "POINT(0 0)")

    def test_listing_model(self):
        listing = self.listing
        self.assertEqual(str(listing), "Test Listing")
        self.assertEqual(listing.title, "Test Listing")
        self.assertEqual(listing.description, "Test description")
        self.assertEqual(listing.price, 100)
        self.assertEqual(listing.email, "test@example.com")
        self.assertEqual(listing.phone, "1234567890")
        self.assertEqual(listing.address, "Test Address")
        self.assertEqual(listing.owner, self.user)
        self.assertEqual(listing.neighborhood, self.neighborhood)
