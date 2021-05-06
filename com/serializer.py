from rest_framework import serializers
from .models import Users,Category,Product,product_image,Order,product_image1
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Users.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ( 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Users.objects.create(
            
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class product_imageSerializer(serializers.ModelSerializer):
    class Meta:
        model=product_image
        fields='__all__'

class product_image_Serializer(serializers.ModelSerializer):
    class Meta:
        model=product_image
        fields=["image"]
class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source='category' ,read_only=True)
    images=product_image_Serializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=("id","product_name","price",
        "description",
        "category","category_name","images")


class CategorySerializer1(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['cat_name']
class OrderSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user' ,read_only=True)
    product_name=serializers.CharField(source='product' ,read_only=True)
    class Meta:
        model=['user','product','user_name','product_name']

class product_imageSerializer1(serializers.ModelSerializer):
    class Meta:
        model=product_image1
        fields='__all__'
    
    def create(self, validated_data):
        user = product_image1.objects.create(
            
            image_name=validated_data['image_name'],
            image=validated_data['image'],
            product=list(validated_data['product'])
        )
        user.save()

        return user