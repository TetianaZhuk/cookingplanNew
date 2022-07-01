from django.contrib import admin

# Register your models here.
from meals.models import Meal, MealCategory


class MealAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MealCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Meal, MealAdmin),
admin.site.register(MealCategory, MealCategoryAdmin),
