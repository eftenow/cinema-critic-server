from django.contrib.auth import get_user_model, password_validation, authenticate
from django.core import exceptions
from rest_framework import serializers

UserModel = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'repeat_password')

    def create(self, validated_data):
        validated_data.pop('repeat_password', None)
        user = super().create(validated_data)

        password = validated_data.get('password')
        user.set_password(password)
        user.save()

        return user

    def to_representation(self, instance):
        return {}

    def validate(self, data):
        password = data.get('password')
        repeat_password = data.get('repeat_password')

        if password and repeat_password and password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")

        user = UserModel(**data)

        errors = dict()
        try:
            password_validation.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        return data
