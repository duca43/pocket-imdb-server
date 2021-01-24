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
    relative_timestamp = serializers.SerializerMethodField(read_only=True)
    
    def get_relative_timestamp(self, obj):
        return get_timestamp_relative_diff(obj.timestamp.replace(tzinfo=None))

    class Meta:
        model = MovieComment
        fields = ['content', 'user', 'timestamp', 'relative_timestamp']

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
