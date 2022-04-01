from flask import jsonify
from components.utils import helpers
from components.utils import jwt
from components.utils import redis as rs


def login_user(username, password):
    res = rs.read_data(collection='users', key=username)
    if helpers.check_password(password, res['password']):
        return jsonify(jwt.sign_jwt(username)), 200
    else:
        return jsonify({'error': 'Incorrect username or password.'}), 401


def create_user(payload):
    user = rs.read_data('users', payload['username'])
    if user:
        return jsonify({'error': 'Username already taken'}), 409

    payload['password'] = helpers.encrypt_password(payload['password'])
    rs.create_data(collection='users', key=payload['username'], data=payload)
    return jsonify({'status': 'User created.'})


def list_users(collection):
    result = rs.get_all_from_collection(collection)
    return result


def check_user_type(username):
    user = rs.read_data('users', username)
    return user['type']
