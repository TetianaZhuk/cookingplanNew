from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.url = reverse('users:login')
        self.success_ulr = reverse('menu:index')
        User.objects.all().delete()
        User.objects.create(username='Test_user',
                            email='Test_user@email.com',
                            password='password')

    def tests_login_GET(self):
        response = self.c.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('users/login.html')

    def tests_login_POST(self):
        response = self.c.post(self.url, username='Test_user', password='password')
        self.assertRedirects(response, self.success_ulr, 302)
        self.assertTemplateUsed('index.html')

