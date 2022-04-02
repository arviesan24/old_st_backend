from flask import Blueprint, request, jsonify
from components.controllers import user_controller as user_ctrl
from components.database.users import check_user_type
from components.utils.jwt import check_token


blueprint = Blueprint('users', __name__)


@blueprint.route("/login", methods=['POST'])
def login():
    return user_ctrl.login_controller(request.get_json())


@blueprint.route("/create-user", methods=['POST'])
def create_user():
    return user_ctrl.create_user_controller(request.get_json())


@blueprint.route("/change-doctor-availability", methods=['POST'])
@check_token
def doctor_availability(user):
    user_type = check_user_type(user['userID'])
    if user_type == 'scheduler':
        return user_ctrl.change_doctor_availability_controller(request.get_json())
    return jsonify({'error': 'Unauthorized access.'}), 401
