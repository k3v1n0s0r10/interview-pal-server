import jwt
import os
from datetime import datetime, timedelta
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from .serializers import RegisterSerializer, LoginSerializer
from .models import UserModel


class UserViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            userFound = UserModel.objects.get(email=data['email'])
        except UserModel.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(data['password'], userFound.password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

        token = self.generateJwt(
            email=userFound.email, username=userFound.username, is_admin=userFound.is_admin)

        return Response(token, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        token = self.generateJwt(
            email=serializer['email'], username=serializer['username'], is_admin=serializer['is_admin'])

        return Response(token, status=status.HTTP_201_CREATED)

    def generateJwt(self, username: str = None, email: str = None, is_admin: bool = None):
        now = datetime.utcnow()
        exp = now + timedelta(minutes=15)

        return jwt.encode({
            'username': username,
            'email': email,
            'isAdmin': is_admin,
            "exp": exp
        },
            os.environ.get('SECRET_KEY'),
            algorithm='HS256')
