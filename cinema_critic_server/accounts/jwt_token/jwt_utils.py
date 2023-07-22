# import jwt
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework import status
# from django.http import JsonResponse
# from django.conf import settings
#
#
# UserModel = get_user_model()
#
#
# def authenticate_with_token(request, raw_token):
#     try:
#         payload = jwt.decode(raw_token, settings.SECRET_KEY, algorithms=['HS256'])
#         return (UserModel.objects.filter(id=payload['user_id']).first(), raw_token)
#     except jwt.ExpiredSignatureError:
#         return None
#
#
# def handle_token_expired(request):
#     raw_refresh_token = request.COOKIES.get('refresh')
#     if raw_refresh_token is None:
#         return None
#
#     try:
#         refresh_token = RefreshToken(raw_refresh_token)
#         return refresh_access_token(request, refresh_token)
#     except TokenError:
#         return JsonResponse({'error': 'Invalid or expired token.'}, status=status.HTTP_401_UNAUTHORIZED)
#
#
# def refresh_access_token(request, refresh_token):
#     new_access_token = str(refresh_token.access_token)
#     response = JsonResponse({'detail': 'Token refreshed'}, status=200)
#     response.set_cookie('access', new_access_token)
#     request.COOKIES['access'] = new_access_token
#     return JWTAuthentication().authenticate(request)