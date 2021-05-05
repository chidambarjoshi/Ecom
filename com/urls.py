

from .views import register,login_api,logout,CategoryView,ProductView,product_imageView
from rest_framework.routers import DefaultRouter
from django.urls import path,include
router = DefaultRouter()
router.register(r'category', CategoryView)
# router.register(r'product', ProductView)
# router.register(r'product_image', product_imageView)



urlpatterns = [
    path('',include(router.urls)),
    path('api/register',register),
    path('api/login',login_api),
    path('api/logout',logout),
    
]
