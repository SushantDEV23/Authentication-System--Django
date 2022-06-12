from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .helpers import send_forgot_mail

# @login_required(login_url='/')           #decorator so that the user must login to access the home page
def home(request):
    return render(request, 'home.html')

def register(request):

    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:

        #checking if the user already exists through name
            if User.objects.filter(username=username).first():
                messages.success(request,'Username already exist.')
                return redirect('/register')
        #checking if the user already exists through email
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email already exist.')
                return redirect('/register')
        #creating user object
            user_obj=User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
        #creating profile object
            profile_obj=Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            # print(password)
            mail_after_registration(email, auth_token)

            return redirect('/token_send')

        except Exception as e:
            print(e)
    return render(request, 'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User does not exist')
            return redirect('/login')

        profile_obj=Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Your profile is not verified')
            return redirect('/login')

        user=authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong Password')
            return redirect('/login')
        if user:
            messages.success(request, 'Successfull Login')
            return redirect('/')
        
        login(request, user)
        return redirect('/')
    return render(request, 'login.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def verify_user(request, auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if(profile_obj):
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def mail_after_registration(email, token):
    subject= "Pending Account Verification"
    message=f"Hi! Your account needs to verified paste the link to verify http://127.0.0.1:8000/verify/{token}"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject, message, email_from, recipient_list)

def error(request):
    return render(request, 'error.html')

def change_password(request, token):
    context={}
    try:

        profile_obj=Profile.objects.get(forgot_password_token=token)
        context={
            'user_id': profile_obj.user.id
        }
        print(profile_obj)

        if request.method=='POST':
            new_password=request.POST.get('new_password')
            re_password=request.POST.get('re_password')
            user_id=request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'The User does not exist')
                return redirect(f'/change_password/{ token }/')
            
            if new_password!=re_password:
                messages.success(request, 'Both the passwords do not match')
                return redirect('/change_password/{ token }/')

            user_obj=User.objects.get(id=user_id)
            # print(str(id))
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login')

        

    except Exception as e:
        print(e)
    
    return render(request, 'change_password.html', context)


def forgot(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Username does not exist')
                return render('/forgot')

            user_obj=User.objects.get(username=username)
            token=str(uuid.uuid4())
            print(token)
            profile_obj=Profile.objects.get(user=user_obj)
            profile_obj.forgot_password_token=token
            profile_obj.save()
            send_forgot_mail(user_obj, token)
            messages.success(request, 'An email has been sent for setting new Password')
            return redirect('/forgot')
    except Exception as e:
        print(e)
    return render(request, 'forgot.html')