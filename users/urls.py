from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [
    path('register/', register_user , name = 'register_user'),
    path('login/' , TokenObtainPairView.as_view() , name = 'token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view() , name = "token_refresh_view"),
    path('profile/', user_profile , name = 'user_profile'),
    path('logout/' , logout_user , name = "logout_user")

]