from django.db.models import Count, Sum, Q, Case, When, BooleanField
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .models import Movie, MovieLike, Like, MovieComment
from .serializers import MovieSerializer, AddMovieLikeSerializer, AddMovieCommentSerializer, MovieCommentSerializer

class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['genre']

    def get_queryset(self):
        return Movie.objects.annotate(
            likes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.LIKE)), 0),
            dislikes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.DISLIKE)), 0),
            user_liked_or_disliked=Coalesce(Sum('movie_likes__like', filter=Q(movie_likes__user=self.request.user)), 0),
            user_watchlist_count = Count('movie_watchlist__id', filter=Q(movie_watchlist__user=self.request.user)),
            is_in_user_watchlist=Case(When(user_watchlist_count__gt=0, then=True), default=False, output_field=BooleanField()),
            user_watchlist_watched_count = Count('movie_watchlist__id', filter=Q(movie_watchlist__user=self.request.user, movie_watchlist__is_watched=True)),
            did_user_watch=Case(When(user_watchlist_watched_count__gt=0, then=True), default=False, output_field=BooleanField())
        ).order_by('id')

    @action(methods=['POST'], detail=True, url_path='like')
    def like(self, request, pk):
        serializer = AddMovieLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        MovieLike.objects.update_or_create(movie=self.get_object(), user=request.user, defaults={**serializer.data})
        return Response(status=HTTP_200_OK)

    @action(methods=['DELETE'], detail=True, url_path='remove-like')
    def remove_like(self, request, pk):
        movie_likes = MovieLike.objects.filter(movie_id=pk, user=request.user)
        if not movie_likes.exists():
            error = {"not_exists_error": ["There is no like/dislike for chosen movie and user."]}
            return Response(error, status=HTTP_404_NOT_FOUND)    
        movie_likes.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['PATCH'], detail=True, url_path='visits') 
    def increment_visits(self, request, pk):          
        movie = Movie.objects.get(pk=pk)
        movie.visits = movie.visits + 1
        movie.save()
        return Response(status=HTTP_200_OK)

class MovieCommentsViewSet(viewsets.GenericViewSet):

    serializer_class = MovieCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieComment.objects.filter(movie=self.kwargs['movie_pk']).order_by('-created_at')

    def list(self, request, movie_pk):
        page = self.paginate_queryset(self.get_queryset())
        response_serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(response_serializer.data)

    def create(self, request, movie_pk):
        serializer = AddMovieCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_comment = MovieComment.objects.create(**serializer.data, movie_id=movie_pk, user=request.user)
        response_serializer = self.get_serializer(movie_comment)
        return Response(response_serializer.data, status=HTTP_201_CREATED)
