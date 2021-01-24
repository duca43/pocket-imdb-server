from rest_framework import serializers
from .models import Movie, MovieLike, MovieComment
from .utils import get_timestamp_relative_diff

class AddMovieCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieComment
        fields = ['comment']

class MovieCommentSerializer(serializers.ModelSerializer):

    content = serializers.CharField(source='comment')
    user = serializers.StringRelatedField(read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)
    
    def get_timestamp(self, obj):
        return get_timestamp_relative_diff(obj.timestamp.replace(tzinfo=None))

    class Meta:
        model = MovieComment
        fields = ['content', 'user', 'timestamp']

class MovieSerializer(serializers.ModelSerializer):

    likes = serializers.IntegerField(read_only=True, default=0)
    dislikes = serializers.IntegerField(read_only=True, default=0)
    user_liked_or_disliked = serializers.IntegerField(read_only=True, default=0)
    movie_comments = MovieCommentSerializer(many=True, read_only=True)

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
                'visits',
                'movie_comments']

class AddMovieLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLike
        fields = ['like']
