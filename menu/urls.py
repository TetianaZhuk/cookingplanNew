from django.urls import path

from .views import index, DayDeleteView, DayListView, DayCreateView, BreakfastCreateView, LaunchCreateView, \
    DinnerCreateView, ShoppingListView

app_name = 'menu'

urlpatterns = [
    path('', index, name='index'),
    path('list/', DayListView.as_view(), name='list'),
    path('create/', DayCreateView.as_view(), name='create'),
    path('<slug:slug>/create/breakfast', BreakfastCreateView.as_view(), name='create_breakfast'),
    path('<slug:slug>/create/launch', LaunchCreateView.as_view(), name='create_launch'),
    path('<slug:slug>/create/dinner', DinnerCreateView.as_view(), name='create_dinner'),
    path('<slug:slug>/delete/', DayDeleteView.as_view(), name='delete'),
    path('', ShoppingListView.as_view(), name='shopping_list'),

]
