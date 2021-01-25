from rest_framework import serializers
from .models import Movie, MovieLike, MovieComment
from pocketimdb.users.serializers import BasicUserSerializer

class AddMovieCommentSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True, max_length=500)

    class Meta:
        model = MovieComment
        fields = ['content']

class MovieCommentSerializer(serializers.ModelSerializer):

    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = MovieComment
        fields = ['id', 'content', 'user', 'created_at']

class MovieSerializer(serializers.ModelSerializer):

    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    user_liked_or_disliked = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Movie
        fields = ['id', 
                'title',
                'description', 
                'cover_image_url', 
                'genre', 
                'likes', 
                'dislikes', 
                'user_liked_or_disliked', 
                'visits']

class AddMovieLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLike
        fields = ['like']
