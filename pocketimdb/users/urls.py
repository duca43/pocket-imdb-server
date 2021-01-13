from django.urls import path
from rest_framework import routers
from .views import UserViewSet

userRouter = routers.SimpleRouter()
userRouter.register(r'users', UserViewSet)
