from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
import random
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


# Create your views here.

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            print('You are trying to login this user:', user)
            auth.login(request, user)
            messages.success(request, 'User Logged in.')
            return redirect('home')
        else:
            messages.success(request, 'Create User First.')
            return redirect('signup')
    return render(request, 'accounts/signin.html')


def sign_up(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if len(password) == 0 and len(password1) == 0:
            messages.warning(request, "Input Password.!")
        elif len(password) <8:
            messages.warning(request, "Enter At-least 8 Character Password.!")
        else:
            b = []
            if password:
                a = ['@', '$', '%', '&', '*', '#']
                for i in a:
                    if i in password:
                        b.append(i)
            if len(b) != 0:
                
                if password == password1:
                    if User.objects.filter(username=username).exists():
                        messages.warning(request, "Username Already Taken.!")
                    elif User.objects.filter(email=email).exists():
                        messages.warning(request, "Email Already Taken.!")
                    else:
                        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                        user.set_password(password)
                        user.save()
                        messages.success(request, "User Created.")
                        return redirect('signin')
                else:
                    messages.warning(request, "Password Not Matched.")
            else:
                messages.warning(request, "Enter a special character in Password.!")

    return render(request, 'accounts/signup.html')

def sign_out(request):
    auth.logout(request)
    return redirect('signin')

def forget_password(request):
    otp = random.randint(1111,9999)
    if request.method == "POST":
        email = request.POST.get('email')
        send_mail_registration(email, otp)
        user = User.objects.get(email=email)
        if user:
            prof = Profile(user=user, otp=otp)
            prof.save()
        return redirect('verify_otp')

    return render(request, 'accounts/forget_password.html')

def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST['password']
        otp = request.POST['otp']
        user = User.objects.get(email=email)
        if user:
            prof = Profile.objects.get(user=user)
            if prof.otp == otp:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "User Password Changed.")
                return redirect('signin')
            else:
                messages.success(request, "Otp not matched try again.")

    return render(request, 'accounts/verify_otp.html')


def send_mail_registration(email, otp):
    subject = "Account Verification otp"
    message = f'hi your verify otp is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
