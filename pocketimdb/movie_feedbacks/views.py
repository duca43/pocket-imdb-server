from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import MovieFeedback, Movie
from .serializers import AddMovieFeedbackSerializer

class MovieFeedbackViewSet(mixins.CreateModelMixin,
                viewsets.GenericViewSet):

    queryset = MovieFeedback.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AddMovieFeedbackSerializer

    def create(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=HTTP_201_CREATED)