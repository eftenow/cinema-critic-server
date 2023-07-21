import jwt
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from cinema_critic_server.accounts.serializers import RegisterUserSerializer, LoginUserSerializer, UserDetailsSerializer
from cinema_critic_server.accounts.view_validators import authenticate_user

UserModel = get_user_model()

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        user.set_password(serializer.validated_data['password'])
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
    def get(self, request):
        user = request.user
        if user.is_anonymous:
            raise AuthenticationFailed('Unauthenticated!')

        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class LogoutUserView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        response.delete_cookie('access')
        response.data = {
            'message': 'success'
        }
        return response
