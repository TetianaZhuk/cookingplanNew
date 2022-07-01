from django.urls import path

from ingredients.views import IngredientCreateView, IngredientDetailView

app_name = 'ingredients'

urlpatterns = [
    path('create/', IngredientCreateView.as_view(), name='create'),
    path('details/<int:pk>/', IngredientDetailView.as_view(), name='detail'),
]