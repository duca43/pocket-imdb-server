from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'cover_image_url', 'genre', 'likes', 'dislikes', 'user_feedback']

    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    user_feedback = serializers.BooleanField(read_only=True, default=None)