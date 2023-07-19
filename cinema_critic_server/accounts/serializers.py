from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from cinema_critic_server.accounts.validators import validate_repeat_password_is_equal

UserModel = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'repeat_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        user = data.get('user')
        password = data.get('password')
        repeat_password = data.pop('repeat_password')

        try:
            validate_password(password, user=user)
            validate_repeat_password_is_equal(password, repeat_password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return data



class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
