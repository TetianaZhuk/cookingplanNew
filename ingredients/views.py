from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin

from ingredients.forms import IngredientForm
from ingredients.models import Ingredient


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/create.html'
    extra_context = {'title': 'Добавить новый продукт'}


class IngredientDetailView(FormMixin, DetailView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/update.html'
    context_object_name = 'ingredient'

