from flask import jsonify
from components.database.users import login_user


def login_controller(payload):
    try:
        return login_user(payload['username'], payload['password'])
    except:
        return jsonify({'error': 'Incorrect username or password.'}), 401
