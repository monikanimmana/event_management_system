from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .models import User
from rest_framework.response import Response
from .serializers import *
import json
from django.contrib.auth import authenticate

# Create your views here.
@api_view(["POST"])
def register_user(request):
        serializer = UserRegisterSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                  {"message" : "User account was successfully created"},
                  status=status.HTTP_201_CREATED
                
                )
    
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST )

@api_view(["POST"])
def login_user(request):
      
        serializer = UserLoginSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email = email , password = password)

            if user is not None:
                  return Response(
                        {"message":"Login successful"},
                        status = status.HTTP_200_OK
                  )
            
            return Response(
                  {"error":"Invalid ceredials"},
                  status = status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)