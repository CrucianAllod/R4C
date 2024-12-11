from django.contrib import admin
from django.urls import path

from robots.views import register_robot, success, summary_robots

urlpatterns = [
    path('register/', register_robot, name='register_robot'),
    path('summary_robots/', summary_robots, name='summary_robots'),
    path('succes/', success, name='success')
]
