from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @action(methods=['PATCH'], detail=True, url_path='visits') 
    def increment_visits(self, request, pk):          
        instance = self.get_object()
        visits = {'visits': instance.visits + 1}
        serializer = self.get_serializer(instance, data=visits, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)