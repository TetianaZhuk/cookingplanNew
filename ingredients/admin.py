from django.contrib import admin

# Register your models here.
from ingredients.models import Ingredient

admin.site.register(Ingredient)