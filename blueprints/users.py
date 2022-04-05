from flask import Blueprint, request, jsonify
from components.controllers import user_controller as user_ctrl
from components.database.users import check_user_type
from components.utils.jwt import check_token


blueprint = Blueprint('users', __name__)


@blueprint.route("/users/login", methods=['POST'])
def login():
    return user_ctrl.login_controller(request.get_json())


@blueprint.route("/users/create", methods=['POST'])
def create_user():
    return user_ctrl.create_user_controller(request.get_json())


@blueprint.route("/users/change-doctor-availability", methods=['POST'])
@check_token
def doctor_availability(user):
    if user:
        return user_ctrl.change_doctor_availability_controller(user, request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/users/authenticate")
@check_token
def authenticate(user):
    user_type = check_user_type(user['userID'])
    if user:
        return jsonify({'status': 'OK', 'type': user_type}), 200
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/users/all-doctors")
@check_token
def all_doctors(user):
    if user:
        return user_ctrl.list_doctors_controller()
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/users/doctor/status")
@check_token
def get_my_status(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'doctor':
        return user_ctrl.get_my_status_controller(user['userID'])
    return jsonify({'error': 'Unauthorized access.'}), 401
