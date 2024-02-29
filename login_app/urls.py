from django.contrib import admin
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    # path('user_login', views.user_login, name = "login2"),
    path('loginpage/', views.loginPage, name="loginpage"),
    path('register/', views.registerPage, name="register"),
    path('logoutpage/', views.logoutUser, name="logoutpage"),
    path('verify-email/<str:user_id>/<str:token>/', views.verify_email, name='verify_email'),

]
