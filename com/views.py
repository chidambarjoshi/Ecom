from django.db.models.fields import json
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import RegisterSerializer,CategorySerializer,ProductSerializer,product_imageSerializer,product_imageSerializer1
from rest_framework import exceptions, serializers, viewsets,status
from .models import Users,Category,Product,product_image,product_image1
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes,action
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
import pdb
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
# Create your views here.

@api_view(['GET','POST'])
def register(request):
    try:
        if request.method == 'POST' :
            data={'email':request.data['email'],
                'first_name':request.data['first_name'],
                'last_name':request.data['last_name'],
                'password':request.data['password'],
                'password2':request.data['password2']
            }        
            serializer=RegisterSerializer(data=data)
            if serializer.is_valid():
                user=serializer.save()  
                print(user)           
                token, _ = Token.objects.get_or_create(user=user)
                message="User Created"
                return JsonResponse({'token':token.key,'message':message},safe=False,status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors['email'][0])
                error={}
                if 'password' in serializer.errors:
                    error.update({'password':serializer.errors['password'][0]})
                if 'email' in serializer.errors:
                    error.update({'email':serializer.errors['email'][0]})
                return JsonResponse(error,status=status.HTTP_400_BAD_REQUEST)

    except:
        message="something went wrong"
        return JsonResponse({'message':message},status=status.HTTP_400_BAD_REQUEST)

       
    if request.method == 'GET':
        user=Users.objects.all()
        serializer=RegisterSerializer(user,many=True)
        return JsonResponse(serializer.data,safe=False)

@api_view(['POST'])
def login_api(request):
    try:
        # pdb.set_trace()
        email=request.data['email']
        password=request.data['password']
        user= authenticate(username=email,password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            message="Login Success"
            return JsonResponse({'token':token.key,'message':message},status=status.HTTP_200_OK)
        else:
            message="Invalid Credentials"
            return JsonResponse({'message':message},status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print('hello')
        print(e)
        message="something went wrong"
        return JsonResponse({'message':message},status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return JsonResponse({'message':"User Logged out"},status=status.HTTP_200_OK)

class CategoryView(viewsets.ModelViewSet):
    search_fields=['cat_name']
    filter_backends=[SearchFilter]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(methods=['get'],detail=False)
    def search(self,request):
        try:
            cat_name=request.data['search']
            category=Category.objects.filter(cat_name__icontains=cat_name).values_list('cat_name',flat= True)
            if category:
                category={'category':list(category)}
                return JsonResponse(data=category,status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message":"category not found"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            message="something went wrong"
            return JsonResponse({'message':message},status=status.HTTP_400_BAD_REQUEST)

class CategoryView1(viewsets.ModelViewSet):
    search_fields=['cat_name']
    filter_backends=[SearchFilter]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductView(viewsets.ModelViewSet):
    search_fields=['product_name']
    filter_backends=[SearchFilter]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related('category')


class product_imageView(viewsets.ModelViewSet):
    serializer_class = product_imageSerializer
    queryset = product_image.objects.all()



class product_imageView1(viewsets.ModelViewSet):
    serializer_class = product_imageSerializer1
    queryset = product_image1.objects.all()

    def create(self, request):
        data=request.data
        try:
            new_product_image=product_image1.objects.create(image=data['image'],image_name=data['image_name'])
            new_product_image.save()
           
            for pro in eval(data['product']):
                pro_obj=Product.objects.get(pk=pro)
                new_product_image.product.add(pro_obj)

            serializers=product_imageSerializer1(new_product_image)

            return JsonResponse(serializers.data,status=status.HTTP_200_OK)
        except:
            print(serializers.errors)
            return JsonResponse({'message':"somthing went wrong"},status=status.HTTP_400_BAD_REQUEST)


