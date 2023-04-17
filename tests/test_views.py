from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.services.models import Business
from users.marketplace.models import Listing
from neighborhood.models import Neighborhood


########################################
# bam.views
########################################


########################################
# users.views
########################################


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
        self.assertContains(response, "user account")
        self.assertTemplateUsed(response, "users/index.html")

    def test_user_account_view_requires_login(self):
        response = self.client.get(reverse("user_account"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/")


class AccountRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_account_register_view_get(self):
        response = self.client.get(reverse("account_register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account register")
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

    def test_account_register_view_post_passwords_dont_match(self):
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
        self.assertContains(response, "account login")
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
        self.assertContains(response, "account delete")
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
        self.assertContains(response, "update account")
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
        self.assertContains(response, "update password")
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


########################################
# users.services.views
########################################


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
        self.assertContains(response, "Add Business")
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


########################################
# users.marketplace.views
########################################


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
        self.assertContains(response, "Add Listing")
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
        self.assertRedirects(response, reverse("view_listing", args=[1]))
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


########################################
# neighborhood.views
########################################


class NeighborhoodsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Neighborhood.objects.create(
            name="Test Neighborhood",
            borough="Test Borough",
            description="Test description",
            lat=40.7128,
            lon=-74.0060,
        )

    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )

    def test_neighborhoods_view(self):
        # Issue a GET request.
        response = self.client.get(reverse("neighborhoods"))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the list of neighborhoods.
        self.assertIn("neighborhoods", response.context)
        neighborhoods = response.context["neighborhoods"]
        self.assertEqual(neighborhoods.count(), 1)

    def test_neighborhood_view(self):
        # Issue a GET request.
        neighborhood = Neighborhood.objects.first()
        response = self.client.get(reverse("neighborhood", args=[neighborhood.pk]))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the neighborhood.
        self.assertIn("neighborhood", response.context)
        self.assertEqual(response.context["neighborhood"], neighborhood)

    def test_borough_view(self):
        # Issue a GET request.
        response = self.client.get(reverse("borough", args=["Test Borough"]))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the borough and its neighborhoods.
        self.assertIn("borough", response.context)
        self.assertIn("neighborhoods", response.context)
        borough = response.context["borough"]
        neighborhoods = response.context["neighborhoods"]
        self.assertEqual(borough, "Test Borough")
        self.assertEqual(neighborhoods.count(), 1)

    def test_authenticated_user_view(self):
        # Create an authenticated user
        self.client.login(username="testuser@example.com", password="password")

        # Issue a GET request to neighborhoods view.
        response = self.client.get(reverse("neighborhoods"))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Issue a GET request to neighborhood view.
        neighborhood = Neighborhood.objects.first()
        response = self.client.get(reverse("neighborhood", args=[neighborhood.pk]))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Issue a GET request to borough view.
        response = self.client.get(reverse("borough", args=["Test Borough"]))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains the authenticated user's first name.
        self.assertIn("firstname", response.context)
        self.assertIsNotNone(response.context["firstname"])
