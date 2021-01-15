from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name']
    
    email = serializers.CharField(required=True, max_length=255)
    name = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, min_length=6, max_length=128, write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']