from flask import Blueprint, request
from components.controllers import user_controller as user_ctrl


blueprint = Blueprint('users', __name__)


@blueprint.route("/login", methods=['POST'])
def login():
    return user_ctrl.login_controller(request.get_json())


@blueprint.route("/create-user", methods=['POST'])
def create_user():
    return user_ctrl.create_user_controller(request.get_json())
