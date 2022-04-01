from flask import request
from functools import wraps
import jwt
import time
from decouple import config

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')


def token_response(token):
    return {
        'access_token': token
    }


def sign_jwt(user_id):
    payload = {
        'userID': user_id,
        'expiry': time.time() + 604800
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token \
            if decode_token['expiry'] >= time.time() \
            else {'error': 'Invalid token. Please log in again.'}
    except jwt.ExpiredSignatureError:
        return {'error': 'Signature expired. Please log in again.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token. Please log in again.'}


def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        result = decode_jwt(token)
        if result.get('error'):
            return result
        return f(*args, **kwargs)

    return decorated
