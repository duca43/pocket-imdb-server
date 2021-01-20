from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer
from .utils import append_movie_feedbacks

class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        page = self.paginate_queryset(queryset)

        for movie in page:
            append_movie_feedbacks(movie, request.user)
        
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        append_movie_feedbacks(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)