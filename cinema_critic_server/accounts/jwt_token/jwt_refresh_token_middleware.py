import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

from rest_framework_simplejwt.exceptions import TokenError


class JwtRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # checking whether there is an existing token already
        token = request.COOKIES.get('access')
        if token:
            # decode the token and check if it's expiring
            decoded = jwt.decode(token, options={"verify_signature": False})
            if datetime.fromtimestamp(decoded['exp']) - datetime.now() < timedelta(minutes=5):
                try:
                    """
                     If its about to expire, we refresh it (I set it up to expire every 5 minutes,  
                     and to refresh for the next 60 minutes after receivign the initial token.)
                     """
                    refresh = RefreshToken(request.COOKIES.get('refresh'))
                    request.COOKIES['access'] = str(refresh.access_token)

                except TokenError:
                    """
                    If both jwt and the refresh token are expired (meaning 1 hr from the initial
                    token has passed), then they both get deleted, so the user has to log back in.
                    """
                    if 'refresh' in request.COOKIES:
                        del request.COOKIES['refresh']
                        del request.COOKIES['access']

        response = self.get_response(request)

        """
        Upon refreshing the jwt token, we also pass it to the response cookies, so that
        the new access (jwt) token is used upon making requests.
        """
        new_access = request.COOKIES.get('access')
        if new_access:
            response.set_cookie('access', new_access, httponly=True)

        return response
