from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(mixins.ListModelMixin,
                viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]