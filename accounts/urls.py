from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views          #this import is for forgot password functionality

urlpatterns = [
    path('', home, name='home'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('success', success, name='success'),
    path('token_send', token_send, name='token_send'),
    path('error', error, name='error'),
    path('verify/<auth_token>', verify_user, name='verify_user'),
    path('forgot', forgot, name='forgot_password'),
    path('change_password/<token>/', change_password, name='change_password')
]

