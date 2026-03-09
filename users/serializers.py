from rest_framework import serializers
from .models import * 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone_number",
            "email",

        ]

        extra_kwargs = {
            "password" : { "write_only" : True }
        }

        def create(self , validated_data):
            user = User.objects.create_user(**validated_data)

            return user
        
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        ]

class UserLogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def save(self):

        refresh_token = self.validated_data["refresh"]
        refresh_object = RefreshToken(refresh_token)
        refresh_object.blacklist()

current_user = get_user_model()

class UserForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_mail(self, value):
         if not current_user.objects.filter(email=value).exists():
             raise serializers.ValidationError("user with this email does not exists.")
         
         return value
    
class UserResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, min_length = 6)
    







