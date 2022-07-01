from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from meals.models import Meal, MealCategory


class MealsListTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.url = reverse('meals:list')
        Meal.objects.all().delete()
        User.objects.all().delete()
        MealCategory.objects.all().delete()
        self.user1 = User.objects.create(username='Test_user1',
                                         email='Test_user1@email.com',
                                         password='test_password1')
        self.user2 = User.objects.create(username='Test_user2',
                                         email='Test_user2@email.com',
                                         password='test_password2')
        self.meal_cat1 = MealCategory.objects.create(name='test_category1')
        self.meal_cat2 = MealCategory.objects.create(name='test_category2')
        self.meal1 = Meal.objects.create(author=self.user1,
                                         name='test_meal1',
                                         category_id=self.meal_cat1.id,
                                         servings=1)
        self.meal2 = Meal.objects.create(author=self.user2,
                                         name='test_meal2',
                                         category_id=self.meal_cat2.id,
                                         servings=2)

    def test_meals_list_page_show_correct_context(self):
        self.assertEqual(2, Meal.objects.count())
        response = self.c.get(self.url)
        self.assertEqual(2, len(response.context['meals']))
        first_meal = response.context['meals'][0]
        self.assertEqual(first_meal.author.username, 'Test_user1')
        self.assertEqual(first_meal.name, 'test_meal1')
        self.assertEqual(first_meal.category.name, 'test_category1')
        self.assertEqual(first_meal.servings, 1)
        self.assertEqual(first_meal.slug, 'test_meal1')
        self.assertEqual(MealCategory.objects.count(), len(response.context['cats']))
        first_category = response.context['cats'][0]
        self.assertEqual(first_category.name, 'test_category1')
        self.assertEqual(first_category.slug, 'test_category1')

    def test_meals_list_page_show_correct_context_if_search_by_category_is_used(self):
        self.assertEqual(2, Meal.objects.count())
        response = self.c.get(self.url + '?category=test_category1')
        self.assertEqual(1, len(response.context['meals']))

    def test_meals_list_page_show_correct_context_if_search_by_query_is_used(self):
        self.assertEqual(2, Meal.objects.count())
        response = self.c.get(self.url + '?q=test_meal')
        self.assertEqual(2, len(response.context['meals']))
        response = self.c.get(self.url + '?q=test_meal1')
        self.assertEqual(1, len(response.context['meals']))
        response = self.c.get(self.url + '?q=test_meal3')
        self.assertEqual(0, len(response.context['meals']))

# class NewBlogTestCase(TestCase):
#
#     def setUp(self):
#         self.c = Client()
#         self.url = reverse('blog:create')
#         category = Category.objects.create(name='Test_category')
#         tag1 = Tag.objects.create(name='#test_tag1')
#         tag2 = Tag.objects.create(name='#test_tag2')
#         Post.objects.all().delete()
#         User.objects.all().delete()
#         Group.objects.create(name='blog_editor')
#         self.user = User.objects.create(username='Test_user',
#                                         email='Test_user@email.com',
#                                         password='password')
#         self.post_data = {'author': self.user,
#                           'title': 'Test',
#                           'draft': True,
#                           'category': category,
#                           'content': 'test',
#                           'image': }
#
#     def test_post_create_user_is_not_authenticate(self):
#         self.assertEqual(0, Post.objects.count())
#         response = self.c.post(self.url, self.post_data)
#         self.assertEqual(302, response.status_code)
#         self.assertEqual(0, Post.objects.count())
#
#     def test_post_create_user_is_authenticate(self):
#         self.assertEqual(0, Post.objects.count())
#         self.c.force_login(self.user)
#         response = self.c.post(self.url, self.post_data)
#         # Post.objects.create(self.post_data)
#         print(response.__dict__)
#         # self.assertEqual(str(response.context['user']), 'Test_user')
#         self.assertEqual(302, response.status_code)
#         self.assertEqual(1, Post.objects.count())
