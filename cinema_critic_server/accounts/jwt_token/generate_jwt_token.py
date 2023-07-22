import jwt, datetime

from cinema_critic_server import settings


def generate_jwt_token(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
