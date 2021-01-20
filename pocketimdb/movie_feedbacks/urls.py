from django.urls import path
from rest_framework import routers
from .views import MovieFeedbackViewSet

movieFeedbacksRouter = routers.SimpleRouter()
movieFeedbacksRouter.register(r'movie_feedbacks', MovieFeedbackViewSet)