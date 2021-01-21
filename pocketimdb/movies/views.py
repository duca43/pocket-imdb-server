from django.db.models import Count, Sum, Q, functions, F, Case, When
from django.db.models.functions import Coalesce
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from .models import Movie, MovieLike
from .serializers import MovieSerializer, AddMovieLikeSerializer

class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        return Movie.objects.annotate(
            likes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=MovieLike.Like.LIKE)), 0),
            dislikes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=MovieLike.Like.DISLIKE)), 0),
            user_liked_or_disliked=Coalesce(Sum('movie_likes__like', filter=Q(movie_likes__user=self.request.user)), 0),
        ).order_by('id')

    @action(detail=True, url_path='likes')
    def like(self, request, pk):
        pass

    @like.mapping.post
    def add_like(self, request, pk):
        serializer = AddMovieLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Movie.objects.filter(pk=pk, movie_likes__user=request.user).exists():
            error = {"unique_together_error": ["Fields movie and user must make a unique set."]}
            return Response(error, status=HTTP_403_FORBIDDEN)
        MovieLike.objects.create(**serializer.data, movie_id=pk, user=request.user)
        return Response(status=HTTP_201_CREATED)

    @like.mapping.patch
    def flip_like(self, request, pk):
        movie_likes = MovieLike.objects.filter(movie_id=pk, user=request.user)
        if len(movie_likes) == 0:
            error = {"not_exists_error": ["There is no like/dislike for chosen movie and user."]}
            return Response(error, status=HTTP_400_BAD_REQUEST)    
        movie_likes.update(like=Case(When(like=MovieLike.Like.LIKE, then=MovieLike.Like.DISLIKE), default=MovieLike.Like.LIKE))
        return Response(status=HTTP_200_OK)

    @like.mapping.delete
    def remove_like(self, request, pk):
        movie_likes = MovieLike.objects.filter(movie_id=pk, user=request.user)
        if len(movie_likes) == 0:
            error = {"not_exists_error": ["There is no like/dislike for chosen movie and user."]}
            return Response(error, status=HTTP_400_BAD_REQUEST)    
        movie_likes.delete()
        return Response(status=HTTP_204_NO_CONTENT)