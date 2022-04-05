from flask import jsonify
from components.utils import helpers
from components.utils import jwt
from components.utils import redis as rs


def login_user(username, password):
    res = rs.read_data(collection='users', key=username)
    if helpers.check_password(password, res['password']):
        token_response = jwt.sign_jwt(username)
        user_data = {'user': res['username'], 'type': res['type']}
        merged_data = {**token_response, **user_data}
        return jsonify(merged_data), 200
    else:
        return jsonify({'error': 'Incorrect username or password.'}), 401


def create_user(payload):
    user = rs.read_data('users', payload['username'])
    if user:
        return jsonify({'error': 'Username already taken'}), 409

    payload['password'] = helpers.encrypt_password(payload['password'])
    rs.create_data(collection='users', key=payload['username'], data=payload)
    return jsonify({'status': 'User created.'})


def list_users():
    result = rs.get_all_from_collection('users')
    return result


def check_user_type(username):
    user = rs.read_data('users', username)
    return user['type']


def __list_doctors():
    result = list_users()
    output = [user for user in result if user['type']=='doctor']
    return output


def list_doctors():
    result = list_users()
    output = [user for user in result if user['type']=='doctor']
    return jsonify({'data': output})


def search_doctor(username):
    doctors = __list_doctors()
    for doctor in doctors:
        if doctor['username'] == username:
            return doctor
    return {}


def is_doctor_available(username):
    doctor = search_doctor(username)
    if doctor.get('available') == True:
        return True
    return False


def change_doctor_availability(username, available):
    try:
        doctor = search_doctor(username)
        doctor['available'] = available
        rs.create_data('users', username, doctor)
        return jsonify({'status': 'Doctor availability changed.'})
    except:
        return jsonify({'error': 'Error changing doctor availability.'})
