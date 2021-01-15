from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name']
    
    name = serializers.CharField(required=True)

    def validate(self, data):
        if len(data['password']) < 6:
            raise serializers.ValidationError({"password": "Password is too short!"})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']