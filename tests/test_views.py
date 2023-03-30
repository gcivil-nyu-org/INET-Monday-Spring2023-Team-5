from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

from users.models import Business, Listing
from neighborhood.models import Neighborhood

from users.views import update_user


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("user_dashboard")

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
        self.assertRedirects(response, reverse("user_dashboard"))

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
        self.assertRedirects(response, reverse("user_dashboard"))
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


class TestDeleteUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User",
        )

    def test_delete_user_unauthenticated(self):
        response = self.client.get(reverse("delete_user"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    def test_delete_user_wrong_password(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.post(reverse("delete_user"), {"password": "wrongpass"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/delete_user.html")
        self.assertEqual(response.context["message"], "Wrong password")
        self.assertEqual(response.context["firstname"], "Test")
        self.assertEqual(response.context["page"], "user-delete")

    def test_delete_user_correct_password(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.post(reverse("delete_user"), {"password": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/logout.html")
        self.assertEqual(response.context["message"], "Account Deleted")
        self.assertEqual(response.context["firstname"], "Test")
        self.assertEqual(response.context["page"], "user-delete")
        self.assertFalse(User.objects.filter(username="testuser").exists())


class UpdateUserViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
        )

    def test_update_user_unauthenticated(self):
        response = self.client.get(reverse("update_user"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    def test_update_user_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(reverse("update_user"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/update_user.html")

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

    def test_add_business_view_post_success(self):
        data = {
            "name": "Test Business",
            "address": "123 Main St.",
            "email": "test@example.com",
            "phone": "555-555-1212",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("view_my_businesses"))
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
            address="Test Address",
            owner=self.user,
            email="test@example.com",
            phone="1234567890",
        )

    def test_view_business_view_unauthenticated(self):
        response = self.client.get(reverse("view_business", args=[self.business.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    def test_view_business_view_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(reverse("view_business", args=[self.business.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/view_business.html")
        self.assertEqual(response.context["message"], "View your business.")
        self.assertEqual(response.context["business"], self.business)


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
        self.url = reverse("services")

    def test_view_all_businesses_view(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertContains(response, "123 Main St")
        self.assertContains(response, "Test Business 2")
        self.assertContains(response, "456 Maple St")


class ViewMyBusinessesViewTestCase(TestCase):
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
        self.url = reverse("view_my_businesses")

    def test_view_my_businesses_view(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Business 1")
        self.assertContains(response, "123 Main St")
        self.assertContains(response, "Test Business 2")
        self.assertContains(response, "456 Maple St")


class TestAddListingView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
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

    def test_add_listing_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        data = {
            "title": "Test Listing",
            "description": "Test description",
            "price": 100,
            "email": "test@example.com",
            "phone": "1234567890",
            "address": "Test Address",
            "neighborhood": self.neighborhood.id,
        }
        response = self.client.post(reverse("add_listing"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("view_listing", args=[1]))
        self.assertEqual(Listing.objects.count(), 1)
        listing = Listing.objects.first()
        self.assertEqual(listing.title, "Test Listing")
        self.assertEqual(listing.description, "Test description")
        self.assertEqual(listing.price, 100)
        self.assertEqual(listing.email, "test@example.com")
        self.assertEqual(listing.phone, "1234567890")
        self.assertEqual(listing.address, "Test Address")
        self.assertEqual(listing.owner, self.user)
        self.assertEqual(listing.neighborhood, self.neighborhood)

    def test_add_listing_unauthenticated(self):
        data = {
            "title": "Test Listing",
            "description": "Test description",
            "price": 100,
            "email": "test@example.com",
            "phone": "1234567890",
            "address": "Test Address",
            "neighborhood": self.neighborhood.id,
        }
        response = self.client.post(reverse("add_listing"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))
        self.assertEqual(Listing.objects.count(), 0)

    def test_add_listing_view_get_request_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(reverse("add_listing"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/add_listing.html")
        neighborhoods = Neighborhood.objects.all()
        self.assertQuerysetEqual(
            response.context["neighborhoods"],
            neighborhoods,
            transform=lambda x: x,
            ordered=False,
        )
        self.assertEqual(response.context["firstname"], "Test")
        self.assertEqual(response.context["page"], "user-add-listing")


class TestViewListingView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
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
            description="Test description",
            price=100,
            email="test@example.com",
            phone="1234567890",
            address="Test Address",
            owner=self.user,
            neighborhood=self.neighborhood,
        )

    def test_view_listing_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(reverse("view_listing", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Listing")
        self.assertContains(response, "Test description")
        self.assertContains(response, "test@example.com")
        self.assertContains(response, "1234567890")
        self.assertContains(response, "Test Address")
        self.assertContains(response, "Test User")

    def test_view_listing_unauthenticated(self):
        response = self.client.get(reverse("view_listing", args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))


class TestMarketplaceView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            email="testuser@example.com",
            password="password",
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

    def test_marketplace_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/marketplace.html")
        listings = Listing.objects.all()
        self.assertQuerysetEqual(
            response.context["listings"],
            listings,
            transform=lambda x: x,
            ordered=False,
        )
        self.assertEqual(response.context["firstname"], "Test")
        self.assertEqual(response.context["page"], "marketplace")

    def test_marketplace_unauthenticated(self):
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))


class TestViewBusinessDetailsView(TestCase):
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
            address="Test Address",
            owner=self.user,
            email="test@example.com",
            phone="1234567890",
        )

    def test_view_business_details_unauthenticated(self):
        response = self.client.get(reverse("view_business_details", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/business_details.html")
        self.assertEqual(response.context["business"], self.business)
        self.assertEqual(response.context["page"], "business-details")
        self.assertNotIn("firstname", response.context)

    def test_view_business_details_authenticated(self):
        self.client.login(username="testuser@example.com", password="password")
        response = self.client.get(
            reverse("view_business_details", args=[self.business.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/business_details.html")
        self.assertEqual(response.context["business"], self.business)
        self.assertEqual(response.context["page"], "business-details")
        self.assertEqual(response.context["firstname"], "Test")
