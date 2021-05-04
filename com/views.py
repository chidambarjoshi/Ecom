from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import RegisterSerializer
from rest_framework import exceptions, viewsets,status
from .models import Users
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
import pdb
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET','POST'])
def register(request):
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