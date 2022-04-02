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


def change_doctor_availability_controller(user, payload):
    user_type = usr.check_user_type(user['userID'])
    doctor = None
    if user_type == 'doctor':
        if user['userID'] != payload.get('doctor'):
            return jsonify({'error': 'You are only allowed to change your own status.'}), 401
        else:
            doctor = user['userID']
    elif user_type == 'scheduler':
        doctor = payload.get('doctor')

    availability = payload.get('available')
    if availability is None:
        return jsonify({'error': 'Availability is required.'}), 400
    if availability is not True and availability is not False:
        return jsonify({'error': 'Availability should be a boolean.'}), 400

    if doctor is None:
        return jsonify({'error': 'Doctor is required.'}), 400
    doctor_on_list = usr.search_doctor(doctor)
    if not doctor_on_list:
        return jsonify({'error': 'Doctor is not on the list.'}), 400
    return usr.change_doctor_availability(doctor, availability)
