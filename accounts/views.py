from django.shortcuts import render

# Create your views here.
def forget_password(request):
    return render(request, 'accounts/forget_password.html')


def sign_in(request):
    return render(request, 'accounts/signin.html')


def sign_up(request):
    return render(request, 'accounts/signup.html')
