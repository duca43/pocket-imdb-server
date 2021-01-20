from rest_framework import serializers
from .models import MovieFeedback

class AddMovieFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieFeedback
        fields = ['movie', 'feedback', 'user']