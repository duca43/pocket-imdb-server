from django.urls import path
from rest_framework import routers
from .views import UserViewSet

user_router = routers.SimpleRouter()
user_router.register(r'users', UserViewSet)
