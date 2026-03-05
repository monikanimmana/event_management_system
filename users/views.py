from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.http import JsonResponse
import json

# Create your views here.
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')

        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            phone_number = phone_number,
            email = email,
            password=password
        )

        return JsonResponse({
            "message" : "User account was successfully created",
            "user_id" : user.id
        })