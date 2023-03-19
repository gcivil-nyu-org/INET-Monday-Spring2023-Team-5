from django.test import TestCase
from users.models import Business
from django.contrib.auth.models import User


class BusinessTestCase(TestCase):
    def test_business_creation(self):
        user = User.objects.create_user(username = 'Test', first_name = 'John', last_name = 'Test')
        business = Business.objects.create(name = 'Test Business Name', \
                                           address = '123 Test Ave', \
                                           owner = user, \
                                           email = 'jtest@gmail.com', \
                                           phone = '123-456-7890'
                                           )
        self.assertEqual(business.name, 'Test Business Name')
        self.assertEqual(business.address, '123 Test Ave')
        self.assertEqual(business.owner, user)
        self.assertEqual(business.email, 'jtest@gmail.com')
        self.assertEqual(business.phone, '123-456-7890')
        self.assertTrue(Business.objects.filter(owner=user, name = 'Test Business Name').exists())
