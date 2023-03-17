from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.add_business_url = reverse('add_business')
        self.view_business_url = reverse('view_business', args=[1])
        self.update_password_url = reverse('update_password')
        self.updateuser_url = reverse('updateuser')
        self.delete_user_url = reverse('delete_user')
        self.view_all_businesses_url = reverse('view_all_businesses')


    def test_index_GET_without_login(self):
        response = self.client.get(self.index_url)
        print(response)
        self.assertRedirects(response, '/users/login/')


    def test_login_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_POST(self):
        response = self.client.post(self.register_url, {
            'email': 'test@example.com',
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'testpassword',
            'password2': 'testpassword'}
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/users/')
        saved_user = User.objects.get(username='test@example.com')  #if we get the username,it means database is OK
        self.assertEquals(saved_user.email, 'test@example.com')
        saved_user.delete()


    def test_view_all_businesses_GET(self):
        response = self.client.get(self.view_all_businesses_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/view_all_businesses.html')
