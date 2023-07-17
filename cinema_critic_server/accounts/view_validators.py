from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from cinema_critic_server.accounts.serializers import LoginUserSerializer


def check_if_all_fields_are_filled(*fields):
    for field in fields:
        if not field:
            raise serializers.ValidationError("Please fill in all required fields.")


def check_valid_login_data(request, username, password):
    serializer = LoginUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(username=username, password=password)

    if not user:
        raise AuthenticationFailed('Incorrect login credentials.')

    return user
