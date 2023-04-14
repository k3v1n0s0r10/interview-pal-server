from rest_framework import serializers

from .models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'username', 'password', 'is_admin']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = UserModel
        fields = ['email', 'password']
