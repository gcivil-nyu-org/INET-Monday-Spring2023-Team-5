from django.test import TestCase
from users.models import Business


class BusinessTestCase(TestCase):

    def test_business_creation(self):
        business = Business.objects.create(name='Test Business Name', \
                                           address='123 Test Ave', \
                                           owner='John Test', \
                                           email='jtest@gmail.com', \
                                           phone='123-456-7890'
                                           )
        self.assertEqual(business.name, 'Test Business Name')
        self.assertEqual(business.address, '123 Test Ave')
        self.assertEqual(business.owner, 'John Test')
        self.assertEqual(business.email, 'jtest@gmail.com')
        self.assertEqual(business.phone, '123-456-7890')
