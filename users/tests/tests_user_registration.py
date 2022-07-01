from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.url = reverse('users:register')
        self.redirect_url = reverse('users:secured')
        self.data = {'username': 'Test_user',
                     'email': 'Test_user@email.com',
                     'password': 'password',
                     'password2': 'password'}
        self.not_valid_data = {'username': 'Test_user',
                               'email': 'Test_user@email',
                               'password': 'password',
                               'password2': 'password'}
        User.objects.all().delete()

    def tests_register_GET(self):
        response = self.c.get(self.url)
        self.assertEqual(200, response.status_code)

    def tests_register_POST_form_is_valid(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.c.post(self.url,
                               self.data)
        user = User.objects.first()
        self.assertEqual(200, response.status_code)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'Test_user')
        self.assertTemplateUsed('users/secured.html')


    def tests_register_POST_form_is_not_valid(self):
        self.assertEqual(User.objects.count(), 0)
        response = self.c.post(self.url,
                               self.not_valid_data)
        user = User.objects.first()
        self.assertEqual(200, response.status_code)
        self.assertEqual(User.objects.count(), 0)
        self.assertTemplateUsed('users/register.html')



