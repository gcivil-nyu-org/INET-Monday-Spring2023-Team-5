from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users import views

class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, views.index_view)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, views.login_view)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, views.register_view)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.logout_view)

    def test_add_business_url_resolves(self):
        url = reverse('add_business')
        self.assertEquals(resolve(url).func, views.add_business_view)

    def test_view_business_url_resolves(self):
        url = reverse('view_business', args=[1])
        self.assertEquals(resolve(url).func, views.view_business_view)

    def test_update_password_url_resolves(self):
        url = reverse('update_password')
        self.assertEquals(resolve(url).func, views.update_password)

    def test_updateuser_url_resolves(self):
        url = reverse('updateuser')
        self.assertEquals(resolve(url).func, views.updateuser)

    def test_delete_user_url_resolves(self):
        url = reverse('delete_user')
        self.assertEquals(resolve(url).func, views.delete_user)

    def test_view_all_businesses_url_resolves(self):
        url = reverse('view_all_businesses')
        self.assertEquals(resolve(url).func, views.view_all_businesses_view)

