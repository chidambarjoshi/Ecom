from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import RegisterSerializer
from rest_framework import exceptions, viewsets,status
from .models import Users
from rest_framework.decorators import api_view


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
            serializer.save()
            return JsonResponse(data,safe=False,status=status.HTTP_201_CREATED)
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


