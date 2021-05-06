

from .views import register,login_api,logout,CategoryView,ProductView,product_imageView,product_imageView1
from rest_framework.routers import DefaultRouter
from django.urls import path,include
router = DefaultRouter()
router.register(r'api/category', CategoryView)
router.register(r'api/product', ProductView)
router.register(r'api/product_image', product_imageView)
router.register(r'api/product_image1', product_imageView1)



urlpatterns = [
    path('',include(router.urls)),
    path('api/register',register),
    path('api/login',login_api),
    path('api/logout',logout),
    
]
