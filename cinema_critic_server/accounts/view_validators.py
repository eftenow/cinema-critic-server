from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from cinema_critic_server.accounts.serializers import LoginUserSerializer


def authenticate_user(request, username, password):
    serializer = LoginUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(username=username, password=password)

    if not user:
        raise AuthenticationFailed('Incorrect login credentials.')

    return user
