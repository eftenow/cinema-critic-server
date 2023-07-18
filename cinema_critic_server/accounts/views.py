from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime

from cinema_critic_server.accounts.serializers import RegisterUserSerializer, LoginUserSerializer, UserDetailsSerializer
from cinema_critic_server.accounts.view_validators import check_valid_login_data, check_if_all_fields_are_filled

UserModel = get_user_model()


# Create your views here.
class RegisterUserView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = RegisterUserSerializer


class LoginUserView(APIView):
    serializer_class = LoginUserSerializer
    queryset = UserModel.objects.all()

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        check_if_all_fields_are_filled(username, password)
        user = check_valid_login_data(request, username, password)

        payload = {
            'id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

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
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
