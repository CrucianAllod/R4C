from django.contrib import admin
from django.urls import path

from robots.views import register_robot, success

urlpatterns = [
    path('register/', register_robot, name='register_robot'),
    path('succes/', success, name='success')
]
