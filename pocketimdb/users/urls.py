from django.urls import path
from rest_framework_nested import routers
from .views import UserViewSet, WatchlistViewSet

user_router = routers.SimpleRouter()
user_router.register(r'users', UserViewSet)

user_router_nested = routers.NestedSimpleRouter(user_router, r'users', lookup='user')
user_router_nested.register(r'watchlist', WatchlistViewSet, basename='watchlist')