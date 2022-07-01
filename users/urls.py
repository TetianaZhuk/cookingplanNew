from django.urls import path
from .views import login_view, logout_view, register_view, OnlyForAuthenticatedUsersView

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('secured/', OnlyForAuthenticatedUsersView.as_view(), name='secured')
    ]