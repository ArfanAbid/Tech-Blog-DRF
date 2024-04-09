from django.urls import path
from .views import *

urlpatterns = [
    path('register/',UserRegister.as_view(),name='register-user'),
    path('login/',UserLogin.as_view(),name='login-user'),
    path('logout/',UserLogout.as_view(),name='logout-user'),
]