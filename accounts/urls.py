from django.urls import path
from .views import forget_password,sign_in,sign_up,sign_out,verify_otp

urlpatterns = [
    path('signin/', sign_in, name ='signin'),
    path('signup/', sign_up, name ='signup'),
    path('sign_out/', sign_out, name ='sign_out'),
    path('forget_password/', forget_password, name ='forget_password'),
    path('verify_otp/', verify_otp, name ='verify_otp'),

]