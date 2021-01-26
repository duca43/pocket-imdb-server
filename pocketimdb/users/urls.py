from django.urls import path
from rest_framework_nested import routers
from .views import UserViewSet, WatchlistViewSet

userRouter = routers.SimpleRouter()
userRouter.register(r'users', UserViewSet)

user_router_nested = routers.NestedSimpleRouter(userRouter, r'users', lookup='user')
user_router_nested.register(r'watchlist', WatchlistViewSet, basename='watchlist')