from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from django.urls import reverse
from pytils.translit import slugify

from ingredients.models import Ingredient


class MealIngredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, verbose_name='Продукт', on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name='Количество')
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='meal')

    class Meta:
        unique_together = ('ingredient', 'meal')


class Meal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('MealCategory', verbose_name="Категория", related_name="meal_cat", null=True,
                                 on_delete=models.SET_NULL)
    description = models.TextField(max_length=1000, verbose_name="Описание", blank=True)
    photo = models.ImageField(upload_to='meals', null=True, default=None, blank=True, verbose_name='Фотография')
    servings = models.SmallIntegerField(verbose_name="Кол-во порций", null=True)

    def get_absolute_url(self):
        return reverse('meals:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            print(self.slug)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class MealCategory(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name="Категория блюда")
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
