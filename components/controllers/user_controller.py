from flask import jsonify
from components.database import users as usr


def login_controller(payload):
    try:
        return usr.login_user(payload['username'], payload['password'])
    except:
        return jsonify({'error': 'Incorrect username or password.'}), 401


def create_user_controller(payload):
    if not payload.get('username'):
        return jsonify({'error': 'Username is required.'}), 400
    if not payload.get('email'):
        return jsonify({'error': 'Email is required.'}), 400
    if not payload.get('password'):
        return jsonify({'error': 'Password is required.'}), 400
    # Scheduler or Doctor
    if not payload.get('type'):
        return jsonify({'error': 'User type is required.'}), 400
    if payload['type'].lower() == 'doctor':
        if payload.get('available') == None:
            return jsonify({'error': 'Availability is required.'}), 400
    return usr.create_user(payload)
    