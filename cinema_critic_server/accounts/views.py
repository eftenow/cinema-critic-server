import jwt
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from cinema_critic_server.accounts.generate_jwt_token import generate_jwt_token
from cinema_critic_server.accounts.serializers import RegisterUserSerializer, LoginUserSerializer, UserDetailsSerializer
from cinema_critic_server.accounts.view_validators import authenticate_user

UserModel = get_user_model()


# Create your views here.
class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        user.set_password(serializer.validated_data['password'])
        user.save()

        login_view = LoginUserView()
        response = login_view.post(request)

        return response


class LoginUserView(APIView):
    queryset = UserModel.objects.all()
    serializer_class = LoginUserSerializer

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate_user(request, username, password)
        token = generate_jwt_token(user)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class DetailsUserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # the algorithm has to be passed like a list here, because of the format that decode uses
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = UserModel.objects.filter(id=payload['id']).first()
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class LogoutUserView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
