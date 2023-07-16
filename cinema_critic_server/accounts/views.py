from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from cinema_critic_server.accounts.serializers import RegisterUserSerializer, LoginUserSerializer

UserModel = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer


class LoginUserView(TokenObtainPairView):
    serializer_class = LoginUserSerializer


class LogoutUserView(APIView):
    def get(self, request):
        self.__perform_logout(request)

    def post(self, request):
        self.__perform_logout(request)

    @staticmethod
    def __perform_logout(request):
        print(request.user)
        request.user.auth_token.delete()
        return Response(
            {'message': 'user logged out'}
        )
