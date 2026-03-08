from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from .models import User
from rest_framework.response import Response
from .serializers import *
import json
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated  

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
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username = username , password = password)

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


@api_view(["GET"])
@permission_classes(["IsAuthenticated"])
def user_profile(request):

      user = request.user
      serializer = UserProfileSerializer(user)

      return Response(serializer.data)

@api_view(["POST"])
def logout_user(request):

      serializer = UserLogoutSerializer(data = request.data)

      if serializer.is_valid():
            serializer.save()

            return Response({"message": "Logout successful"},status = status.HTTP_205_RESET_CONTENT)
      
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
