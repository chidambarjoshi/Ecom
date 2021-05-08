from django.urls import path,include
from .views import userregister


urlpatterns={
    path('/register',userregister,name='register')
}