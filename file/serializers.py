from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CSVfiles

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVfiles
        fields = ['file']
