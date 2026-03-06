from rest_framework import serializers
from .models import * 

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


