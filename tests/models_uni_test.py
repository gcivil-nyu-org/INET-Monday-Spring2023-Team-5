from django.test import TestCase
from users.models import Business


class BusinessTestCase(TestCase):

    def test_business_creation(self):
        Business = Business.objects.create(name='Test Business Name', \
                                           address='123 Test Ave', \
                                           owner='John Test', \
                                           email='jtest@gmail.com', \
                                           phone='123-456-7890'
                                           )
        self.assertEqual(Business.name, 'Test Business Name')
        self.assertEqual(Business.address, '123 Test Ave')
        self.assertEqual(Business.owner, 'John Test')
        self.assertEqual(Business.email, 'jtest@gmail.com')
        self.assertEqual(Business.phone, '123-456-7890')
