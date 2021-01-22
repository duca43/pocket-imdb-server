from django.db.models import Count, Sum, Q, functions, F, Case, When
from django.db.models.functions import Coalesce
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from .models import Movie, MovieLike, Like
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
            likes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.LIKE)), 0),
            dislikes=Coalesce(Count('movie_likes__like', filter=Q(movie_likes__like=Like.DISLIKE)), 0),
            user_liked_or_disliked=Coalesce(Sum('movie_likes__like', filter=Q(movie_likes__user=self.request.user)), 0),
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