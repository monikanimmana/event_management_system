from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from .models import User
from rest_framework.response import Response
from .serializers import *
import json
from django.contrib.auth import authenticate , get_user_model
from rest_framework.permissions import IsAuthenticated 
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator



# Create your views here.
def generator_uid_token(user):

      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)

      return uid , token


@api_view(["POST"])
def register_user(request):
        serializer = UserRegisterSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            uid , token = generator_uid_token(user)

            domain = request.get_host()

            verify_link = f"http://{domain}/users/email_verify/{uid}/{token}/"

            return Response(
                  {
                        "message" : "Account created successfully but Email verify is required and sent the link",
                        "verify_link" : verify_link
                  }, 
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


User = get_user_model()

@api_view(["POST"])
def forgot_password(request):

      serializer = UserForgotPasswordSerializer(data = request.data)

      if serializer.is_valid():

            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            uid , token = generator_uid_token(user)
            domain = request.get_host()

            reset_link = f"http://{domain}/users/reset-password/{uid}/{token}/"

            return Response({'messegae':'Password reset link was generated','reset_link' : reset_link})
      
      return Response(serializer.errors)

@api_view(["POST"])
def reset_password(request, uidb64 , token):

      serializer = UserResetPasswordSerializer(data = request.data)

      try:

            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)

      except:
            return Response({"messege": "invalid user"})
      
      if not PasswordResetTokenGenerator().check_token(token):
            return Response({"messege":"token has expired"})
      
      new_password = request.data.get('password')
      user.set_password(new_password)
      user.save()

      return Response({"messege":"Password Reset Successfully"})

@api_view(["GET"])
def email_verify(request , uidb64 , token):

      try :
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(id = uid)

      except:
            return Response({"messege":"invalid user Id"})
      
      if not generator_uid_token(user)[1] == token:
            return Response({"messege":"token expired"})
      
      user.is_active = True
      user.save()

      return Response({"messege":"Email verify successful , You can login now"},
                      status=status.HTTP_200_OK
                      )

      




      

      

