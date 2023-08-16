import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from cinema_critic_server.accounts.serializers import RegisterUserSerializer, LoginUserSerializer, \
    UserDetailsSerializer, EditUserSerializer, UsersListSerializer
from cinema_critic_server.accounts.view_validators import authenticate_user
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


class AllUsersListView(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UsersListSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        user.set_password(serializer.validated_data['password'])

        regular_user_group, created = Group.objects.get_or_create(name='Regular User')
        user.groups.add(regular_user_group)

        user.save()

        tokens = RefreshToken.for_user(user)

        response = Response()
        response.set_cookie(key='refresh', value=str(tokens), httponly=True)
        response.set_cookie(key='access', value=str(tokens.access_token), httponly=True)
        response.data = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
        return response


class LoginUserView(APIView):
    queryset = UserModel.objects.all()
    serializer_class = LoginUserSerializer

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate_user(request, username, password)
        tokens = RefreshToken.for_user(user)

        response = Response()
        response.set_cookie(key='refresh', value=str(tokens), httponly=True)
        response.set_cookie(key='access', value=str(tokens.access_token), httponly=True)
        response.data = {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }
        return response


class DetailsUserView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                user = UserModel.objects.get(pk=pk)
            except UserModel.DoesNotExist:
                raise Http404
        else:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Unauthenticated!')

        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class EditUserProfileView(generics.UpdateAPIView):
    serializer_class = EditUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserModel.objects.all()

    def get_object(self):
        """
        returns the authenticated user's profile unless an admin is
        trying to access another user's profile.
        """
        if self.request.user.groups.filter(name='Administrator').exists() and 'pk' in self.kwargs:
            try:
                # returns the user specified by 'pk'
                return UserModel.objects.get(pk=self.kwargs['pk'])
            except UserModel.DoesNotExist:
                raise Http404("User not found")

        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        returns the serialized data of the user that is returned by get_object
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        returns the authenticated user's profile unless an admin is
        trying to access another user's profile.
        """
        if self.request.user.groups.filter(name='Administrator').exists() and 'pk' in self.kwargs:
            try:
                return UserModel.objects.get(pk=self.kwargs['pk'])
            except UserModel.DoesNotExist:
                raise Http404("User not found")

        """
        if the user trying to edit is not an admin, this returns the currently
        logged-in user's profile, even if he's trying to access another user's profile
        """
        return self.request.user


class LogoutUserView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        response.delete_cookie('access')
        response.data = {
            'message': 'success'
        }
        return response


class CheckUserIsAuthenticatedView(APIView):
    def get(self, request):
        is_authenticated = False
        if request.user:
            is_authenticated = request.user.is_authenticated
        return Response({'isAuthenticated': is_authenticated})
