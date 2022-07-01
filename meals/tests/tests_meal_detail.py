from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from ingredients.models import Ingredient
from meals.models import Meal, MealCategory, MealIngredients


class MealDetailTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.url = reverse('meals:detail', kwargs={'slug': 'test_meal'})
        Meal.objects.all().delete()
        User.objects.all().delete()
        MealCategory.objects.all().delete()
        self.category = MealCategory.objects.create(name='Test_category')
        self.user = User.objects.create(username='Test_user',
                                        email='Test_user@email.com',
                                        password='test_password')
        self.meal = Meal.objects.create(author=self.user,
                                        name='test_meal',
                                        category=self.category,
                                        description='Test_meal description',
                                        servings=1)
        self.ingredient1 = Ingredient.objects.create(name='test_ingredient1', units='кг')
        self.ingredient2 = Ingredient.objects.create(name='test_ingredient2', units='шт')
        self.ingredient3 = Ingredient.objects.create(name='test_ingredient3', units='г')

        self.meal_ingredient1 = MealIngredients.objects.create(ingredient=self.ingredient1,
                                                               qty=1,
                                                               meal=self.meal)
        self.meal_ingredient2 = MealIngredients.objects.create(ingredient=self.ingredient2,
                                                               qty=2,
                                                               meal=self.meal)
        self.meal_ingredient3_data = {'ingredient': self.ingredient3.id,
                                      'qty': 3}

    def test_meal_detail_page_show_correct_context(self):
        self.assertEqual(1, Meal.objects.count())
        self.assertEqual('test_meal', self.meal.slug)
        url = reverse('meals:detail', kwargs={'slug': self.meal.slug})
        response = self.c.get(url)
        meal = response.context['meal']
        self.assertEqual('test_meal', meal.name)
        self.assertEqual('Test_user', meal.author.username)
        self.assertEqual('Test_meal description', meal.description)
        self.assertEqual(1, meal.servings)
        self.assertEqual(2, MealIngredients.objects.count())
        ingredients = response.context['ingredients']
        self.assertEqual(2, len(ingredients))
        first_ingredient = ingredients[0]
        self.assertEqual('test_ingredient1', first_ingredient.ingredient.name)
        self.assertEqual(1, first_ingredient.qty)
        self.assertEqual('кг', first_ingredient.ingredient.units)

    def test_meal_detail_add_meals_ingredients_user_is_not_author(self):
        self.assertEqual(1, Meal.objects.count())
        self.assertEqual(2, MealIngredients.objects.count())
        url = reverse('meals:add_ingredients', kwargs={'slug': self.meal.slug})
        response = self.c.post(url, self.meal_ingredient3_data, follow=True)
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed('meals:detail')

    def test_meal_detail_add_meals_ingredients_user_is_author(self):
        self.c.force_login(self.user)
        self.assertEqual(1, Meal.objects.count())
        self.assertEqual(2, MealIngredients.objects.count())
        url = reverse('meals:add_ingredients', kwargs={'slug': self.meal.slug})
        response = self.c.post(url, self.meal_ingredient3_data, follow=True)
        self.assertEqual(200, response.status_code)
        ingredients = response.context['ingredients']
        self.assertEqual(3, len(ingredients))
        third_ingredient = ingredients[2]
        self.assertEqual('test_ingredient3', third_ingredient.ingredient.name)
        self.assertEqual(3, third_ingredient.qty)
        self.assertEqual('г', third_ingredient.ingredient.units)
        self.assertTemplateUsed('meals:detail')
