
from django.urls import path
from .views import register,login_api,logout



urlpatterns = [
    path('api/register',register),
    path('api/login',login_api),
    path('api/logout',logout)
]