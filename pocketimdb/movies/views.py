from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from .models import Movie, MovieLike, Like, WatchList, MovieWatch
from .serializers import MovieSerializer, AddMovieLikeSerializer, WatchListSerializer, SetMovieWatchSerializer

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
            in_user_watch_list=Count('watchlist__id', filter=Q(watchlist__user=self.request.user)),
            user_watched=Count('moviewatch__watched', filter=Q(watchlist__user=self.request.user, moviewatch__watched=True))
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

class MovieWatchListViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WatchList.objects.get_or_create(user=self.request.user)[0]

    def list(self, request):
        response_serializer = WatchListSerializer(self.get_queryset())
        return Response(response_serializer.data, status=HTTP_200_OK)

class MovieWatchViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MovieWatch.objects.filter(watch_list=self.kwargs['watch_list_pk'])

    def update(self, request, watch_list_pk, pk):
        try:
            MovieWatch.objects.create(movie_id=pk, watch_list_id=watch_list_pk)
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, watch_list_pk, pk):
        try:
            movie_watch = self.get_queryset().get(movie_id=pk)
            movie_watch.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, watch_list_pk, pk):
        serializer = SetMovieWatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            movie_watch = self.get_queryset().get(movie_id=pk)
            movie_watch.watched = serializer.data['watched']
            movie_watch.save()
            return Response(status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)