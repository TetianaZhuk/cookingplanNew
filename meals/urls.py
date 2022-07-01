from django.urls import path

from .views import MealCreateView, MealDetailView, MealsList, MealUpdateView, MealDeleteView, AddMealToDay, \
    AddIngredientsToMeal, MealIngredientsDeleteView

app_name = 'meals'

urlpatterns = [
    path('list/', MealsList.as_view(), name='list'),
    path('create/', MealCreateView.as_view(), name='create'),
    path('<slug:slug>/detail/', MealDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', MealUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', MealDeleteView.as_view(), name='delete'),
    path('<slug:slug>/add_to_day/', AddMealToDay.as_view(), name='add_to_day'),
    path('<slug:slug>/add_ingredients/', AddIngredientsToMeal.as_view(), name='add_ingredients'),
    path('<slug:slug>/delete_ingredient/<int:pk>', MealIngredientsDeleteView.as_view(), name='delete_ingredient'),
]
