from rest_framework import serializers
from .models import * 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


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

current_user = get_user_model
class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = current_user
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number"
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


class UserChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(required = True )
    new_password = serializers.CharField(required = True , write_only = True , validators = [validate_password] )
    confirm_password = serializers.CharField(write_only = True)

    def validate(self, data):

        if self.new_password != self.confirm_password:
            raise serializers.ValidationError({"confirm_password":"Password do not match"})
        
        return data


    
    
     

    

    







