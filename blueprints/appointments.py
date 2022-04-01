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
