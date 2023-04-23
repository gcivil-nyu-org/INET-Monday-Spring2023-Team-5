from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.marketplace.models import Listing
from neighborhood.models import Neighborhood


class MarketplaceViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
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
        self.listing1 = Listing.objects.create(
            title="Test Listing 1",
            description="Test description 1",
            price=100,
            email="test1@example.com",
            phone="1234567890",
            address="Test Address 1",
            owner=self.user,
            neighborhood=self.neighborhood,
        )
        self.listing2 = Listing.objects.create(
            title="Test Listing 2",
            description="Test description 2",
            price=200,
            email="test2@example.com",
            phone="2345678901",
            address="Test Address 2",
            owner=self.user,
            neighborhood=self.neighborhood,
        )

    def test_marketplace_view(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Listing 1")
        self.assertTemplateUsed(response, "marketplace/marketplace.html")
        listings = Listing.objects.all()
        self.assertQuerysetEqual(
            response.context["listings"],
            listings,
            transform=lambda x: x,
            ordered=False,
        )
        self.assertEqual(response.context["firstname"], "Test")
        self.assertEqual(response.context["page"], "marketplace")

    def test_marketplace_view_requires_login(self):
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/marketplace/")


class AddListingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
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

    def test_add_view(self):
        self.client.login(username="testuser@example.com", password="testpass")

        response = self.client.get(reverse("add_listing"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account-add-listing")
        self.assertTemplateUsed(response, "marketplace/add_listing.html")

        data = {
            "title": "Test Listing",
            "description": "Test Description",
            "price": 100,
            "email": "test@example.com",
            "phone": "123-456-7890",
            "address": "123 Test St",
            "neighborhood": self.neighborhood.pk,
        }
        response = self.client.post(reverse("add_listing"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_listings"))
        self.assertEqual(Listing.objects.count(), 1)

    def test_add_view_requires_login(self):
        response = self.client.get(reverse("add_listing"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/listings/add/")


class ViewListingViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
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
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="Test Description",
            address="123 Test St",
            owner=self.user,
            email="test@example.com",
            phone="123-456-7890",
            neighborhood=self.neighborhood,
            price=100,
        )

    def test_view_view(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("view_listing", args=[self.listing.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Listing")
        self.assertTemplateUsed(response, "marketplace/view_listing.html")

    def test_view_view_requires_login(self):
        response = self.client.get(reverse("view_listing", args=[self.listing.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/listings/{}/".format(self.listing.id),
        )


class MarketplaceByBoroughTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.neighborhood1 = Neighborhood.objects.create(
            name="Example Neighborhood 1",
            borough="Borough1",
            description="A test neighborhood.",
            lat=40.7128,
            lon=-74.0060,
        )
        self.neighborhood2 = Neighborhood.objects.create(
            name="Example Neighborhood 2",
            borough="Borough2",
            description="Another test neighborhood.",
            lat=40.7128,
            lon=-74.0060,
        )
        self.listing1 = Listing.objects.create(
            title="Listing 1",
            description="Test listing 1",
            address="123 Example St",
            owner=self.user,
            neighborhood=self.neighborhood1,
            price=1000,
        )
        self.listing2 = Listing.objects.create(
            title="Listing 2",
            description="Test listing 2",
            address="456 Example St",
            owner=self.user,
            neighborhood=self.neighborhood2,
            price=2000,
        )

    def test_marketplace_by_borough(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("marketplace_by_borough", args=["borough1"]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.listing1, response.context["listings"])
        self.assertNotIn(self.listing2, response.context["listings"])


class MyListingsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
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
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="Test Description",
            address="123 Test St",
            owner=self.user,
            email="test@example.com",
            phone="123-456-7890",
            neighborhood=self.neighborhood,
            price=100,
        )

    def test_view_view(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("user_listings"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Listing")
        self.assertTemplateUsed(response, "marketplace/my_listings.html")

    def test_view_view_requires_login(self):
        response = self.client.get(reverse("user_listings"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/listings/")


class DeleteListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
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
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="Test Description",
            address="123 Test St",
            owner=self.user,
            email="test@example.com",
            phone="123-456-7890",
            neighborhood=self.neighborhood,
            price=100,
        )

    def test_delete_Listing(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.get(reverse("delete_listing", args=[self.listing.id]))
        self.assertEqual(Listing.objects.count(), 0)
        self.assertRedirects(response, reverse("user_listings"))

    def test_delete_Listing_requires_login(self):
        response = self.client.get(reverse("delete_listing", args=[self.listing.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/listings/{}/delete/".format(
                self.listing.id
            ),
        )


class UpdateListingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="testpass",
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
        self.listing = Listing.objects.create(
            title="Test Listing",
            description="Test Description",
            address="123 Test St",
            owner=self.user,
            email="test@example.com",
            phone="123-456-7890",
            neighborhood=self.neighborhood,
            price=100,
        )

    def test_update_listing(self):
        self.client.login(username="testuser@example.com", password="testpass")
        response = self.client.post(
            reverse("update_listing", args=[self.listing.id]),
            {
                "title": "New Listing",
                "description": "New Description",
                "address": "123 New St",
                "email": "newtest@example.com",
                "phone": "321-654-0987",
                "neighborhood": self.neighborhood.id,
                "price": 200,
            },
        )

        self.listing.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.listing.title, "New Listing")
        self.assertEqual(self.listing.description, "New Description")
        self.assertEqual(self.listing.address, "123 New St")
        self.assertEqual(self.listing.email, "newtest@example.com")
        self.assertEqual(self.listing.phone, "321-654-0987")
        self.assertEqual(self.listing.price, 200)
        self.assertEqual(self.listing.neighborhood, self.neighborhood)
        
        response = self.client.get(reverse("update_listing", args=[self.listing.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("listing", response.context)
        self.assertEqual(response.context['listing'], self.listing)

    def test_update_Listing_requires_login(self):
        response = self.client.post(
            reverse("update_listing", args=[self.listing.id]),
            {
                "title": "New Listing",
                "description": "New Description",
                "address": "123 New St",
                "email": "test@example.com",
                "phone": "321-654-0987",
                "neighborhood": self.neighborhood,
                "price": 200,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/accounts/listings/{}/update/".format(
                self.listing.id
            ),
        )
