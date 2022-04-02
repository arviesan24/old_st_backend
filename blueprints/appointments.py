from flask import Blueprint, request, jsonify
from components.controllers import appointment_controller as apt_ctrl
from components.database.users import check_user_type
from components.utils.jwt import check_token


blueprint = Blueprint('appointments', __name__)


@blueprint.route("/create-appointment", methods=['POST'])
@check_token
def create(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'scheduler':
        return apt_ctrl.create_appointment_controller(request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/search-appointment", methods=['POST'])
@check_token
def search(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'scheduler':
        return apt_ctrl.search_appointment_controller(request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/update-appointment", methods=['POST'])
@check_token
def update(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'scheduler':
        return apt_ctrl.update_appointment_controller(request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/assign-appointment", methods=['POST'])
@check_token
def assign(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'scheduler':
        return apt_ctrl.assign_appointment_controller(request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/accept-appointment", methods=['POST'])
@check_token
def accept(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'doctor':
        return apt_ctrl.accept_appointment_controller(user['userID'], request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/delete-appointment", methods=['POST'])
@check_token
def delete(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'scheduler':
        return apt_ctrl.delete_appointment_controller(request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/my-appointments")
@check_token
def my_appointments(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'doctor':
        return apt_ctrl.my_appointments_controller(user['userID'])
    return jsonify({'error': 'Unauthorized access.'}), 401


@blueprint.route("/my-appointments-search", methods=['POST'])
@check_token
def my_appointments_search(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'doctor':
        return apt_ctrl.my_appointments_search_controller(user['userID'], request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401
