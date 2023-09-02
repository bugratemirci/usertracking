import jwt
import datetime
from rest_framework import exceptions


def create_access_token(id):
    return jwt.encode({
        'id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        return payload['id']
    except:
        raise exceptions.AuthenticationFailed('Invalid token')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])
        return payload['id']
    except:
        raise exceptions.AuthenticationFailed('Invalid token')


def create_refresh_token(id):
    return jwt.encode({
        'id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')
