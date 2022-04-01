from flask import Flask, jsonify, request
from components.controllers import user_controller as user_ctrl
from components.utils.jwt import check_token


app = Flask(__name__)


@app.route("/")
def main():
    return jsonify({
        'status': 'OK'
    }), 200


@app.route("/login", methods=['POST'])
def login():
    return user_ctrl.login_controller(request.get_json())


@app.route("/create-user", methods=['POST'])
def create_user():
    return user_ctrl.create_user_controller(request.get_json())


if __name__ == '__main__':
    app.run(debug=True)
