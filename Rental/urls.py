from django.contrib import admin
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='Home'),
    path('strona/<str:type>', views.strona1, name='strona1'),
    path('vehicle/<str:pk>', views.vehiclePage, name='VehiclePage'),
    path('add-rental', views.createRental, name='add_rental'),
    path('update-rental/<str:pk>', views.updateRental, name='update_rental'),
    path('delete-rental/<str:pk>', views.deleteRental, name='delete_rental'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('delete-comment/<str:pk>', views.delete_comment, name='delete_comment'),
    path('userprofile/', views.UserProfile, name='userprofile'),
    path('rent-vehicle/<str:pk>', views.startRenting, name='start-rent'),
    path('stop-rent-vehicle/<str:pk>', views.stopRenting, name='stop-rent'),
]
