from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

UserModel = get_user_model()

from django.conf import settings


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get('access')
            if raw_token is None:
                return None

            payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=['HS256'])

            return (UserModel.objects.filter(id=payload['user_id']).first(), raw_token)

        return super().authenticate(request)
