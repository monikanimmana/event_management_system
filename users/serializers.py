from rest_framework import serializers
from .models import * 
from rest_framework_simplejwt.tokens import RefreshToken

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




