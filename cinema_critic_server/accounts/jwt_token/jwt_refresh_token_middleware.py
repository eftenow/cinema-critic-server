import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta


class JwtRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if there is a JWT cookie.
        token = request.COOKIES.get('access')
        if token:
            # Decode the JWT and check if it's about to expire.
            decoded = jwt.decode(token, options={"verify_signature": False})
            if datetime.fromtimestamp(decoded['exp']) - datetime.now() < timedelta(minutes=5):
                # If it is, refresh it.
                refresh = RefreshToken(request.COOKIES.get('refresh'))
                request.COOKIES['access'] = str(refresh.access_token)

        response = self.get_response(request)

        # if token refreshed, add the new access token to the response cookies.
        new_access = request.COOKIES.get('access')
        if new_access:
            response.set_cookie('access', new_access, httponly=True)

        return response
