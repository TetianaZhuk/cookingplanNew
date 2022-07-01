import datetime

from django import forms

from .models import Meal, MealIngredients, Ingredient


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ('author', 'slug',)


class MealIngredientsForm(forms.ModelForm):
    class Meta:
        model = MealIngredients
        exclude = ('meal',)


class AddMealToDayForm(forms.Form):
    CHOICES = (('ЗАВТРАК', 'Завтрак'),
               ('ОБЕД', 'Обед'),
               ('УЖИН', 'Ужин'))
    date = forms.DateField(widget=forms.SelectDateWidget, label='Введите дату', initial=datetime.date.today())
    day_time = forms.ChoiceField(choices=CHOICES, label='Введите прием пищи')
