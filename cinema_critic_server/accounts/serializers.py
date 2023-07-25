from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from cinema_critic_server.accounts.models import Profile
from cinema_critic_server.accounts.validators import validate_repeat_password_is_equal

UserModel = get_user_model()


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email']


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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture', 'gender', 'city', 'country', 'description']


class UserDetailsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class EditUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        """"
        the .update() method does not support writable nested fields by default,
        so  i have to do it manually, since i have my custom 'AppUser' which only
        contains the auth user data, and and additional Model, called 'Profile'
        which holds all the other information regarding the user profile, such as
        first_name, last_name, profile_picture, gender and so on...
        """
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.city = profile_data.get('city', profile.city)
        profile.country = profile_data.get('country', profile.country)
        profile.description = profile_data.get('description', profile.description)
        profile.save()

        return instance
