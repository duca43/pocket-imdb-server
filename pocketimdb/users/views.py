from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from rest_framework.decorators import action
from .serializers import (
    CreateUserSerializer, 
    UserSerializer, 
    AddAndRemoveMovieWatchlistSerializer, 
    UpdateMovieWatchlistSerializer, 
    MovieWatchlistSerializer
)
from .models import MovieWatchlist
from .permission import UserAccessPermission

User = get_user_model()

class UserViewSet(mixins.CreateModelMixin,
                viewsets.GenericViewSet):

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.data)
        return Response(status=HTTP_201_CREATED)

    @action(detail=False, url_path='me', permission_classes=[IsAuthenticated]) 
    def get_current_user(self, request):          
        response_serializer = UserSerializer(request.user)
        return Response(response_serializer.data, HTTP_200_OK)

class WatchlistViewSet(mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, UserAccessPermission]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdateMovieWatchlistSerializer
        return MovieWatchlistSerializer

    def get_queryset(self):
        return MovieWatchlist.objects.filter(user=self.kwargs['user_pk']).order_by('id')

    def create(self, request, user_pk):
        serializer = AddAndRemoveMovieWatchlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_id = serializer.data['movie']
        watchlist_movie = MovieWatchlist.objects.update_or_create(user_id=user_pk, movie_id=movie_id)[0]
        response_serializer = self.get_serializer(watchlist_movie)
        return Response(response_serializer.data, status=HTTP_201_CREATED)