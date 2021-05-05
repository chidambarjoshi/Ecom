from django.contrib import admin
from django.contrib.auth.models import User
from .models import Users,Category,Product,product_image
 # Register your models here.
admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(product_image)