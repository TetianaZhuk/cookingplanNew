import shutil
import tempfile

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase, Client, override_settings

# Create your tests here.
from django.urls import reverse

from cookingplan import settings
from meals.models import Meal, MealCategory
from django.core.files.uploadedfile import SimpleUploadedFile

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CreateMealTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.c = Client()
        self.url = reverse('meals:create')
        Meal.objects.all().delete()
        User.objects.all().delete()
        MealCategory.objects.all().delete()
        self.category = MealCategory.objects.create(name='Test_category')
        self.user = User.objects.create(username='Test_user',
                                        email='Test_user@email.com',
                                        password='test_password')
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.meal_data = {'name': 'Test_meal',
                          'category': self.category.id,
                          'description': 'Test_meal description',
                          'photo': uploaded,
                          'servings': 1}

    def test_create_meal_category_slug(self):
        self.assertEqual(slugify('Test_category'), self.category.slug)

    def test_create_meal_user_is_not_authenticate(self):
        self.assertEqual(0, Meal.objects.count())
        response = self.c.post(self.url, self.meal_data, follow=True)
        self.assertEqual(0, Meal.objects.count())
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed('users:secured')

    def test_create_meal_user_is_authenticate(self):
        self.assertEqual(1, MealCategory.objects.count())
        self.assertEqual(0, Meal.objects.count())
        self.c.force_login(self.user)
        response = self.c.post(self.url, self.meal_data, follow=True)
        self.assertEqual(1, Meal.objects.count())
        user = response.context['user']
        self.assertEqual('Test_user', user.username)
        self.assertEqual(200, response.status_code)
        meal = response.context['meal']
        self.assertEqual('test_meal', meal.slug)
        self.assertEqual('test_category', MealCategory.objects.first().slug)
        self.assertEqual(1, Meal.objects.count())


class UpdateMealTestCase(TestCase):
    def SetUp(self):
        self.c = Client()
        self.url = reverse('meals:update')
        Meal.objects.all().delete()
        User.objects.all().delete()
        MealCategory.objects.all().delete()
        self.user = User.objects.create(username='Test_user',
                                        email='Test_user@email.com',
                                        password='test_password')
        self.category = MealCategory.objects.create(name='Test_category')
        self.meal = Meal.objects.create(author=self.user,
                                        name='Test_meal',
                                        category=self.category,
                                        description='Test_meal description',
                                        servings=1)

    def test_update_meal_user_is_not_authenticate(self):
        self.assertEqual(1, Meal.objects.count())
