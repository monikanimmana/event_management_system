from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class CustomUserAdmins(UserAdmin):
    model = User
    list_display=("id","username","email","phone_number","is_staff","is_active")
    search_fields = ("username","email","phone_number")
    ordering=("id",)

admin.site.register(User,CustomUserAdmins)
