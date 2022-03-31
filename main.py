from flask import Flask, jsonify, request
from components.controllers import controller as ctrl


app = Flask(__name__)


@app.route("/")
def main():
    return jsonify({
        'status': 'OK'
    }), 200


@app.route("/login", methods=['POST'])
def login():
    return ctrl.login_controller(request.get_json())


@app.route("/create-user", methods=['POST'])
def create_user():
    return ctrl.create_user_controller(request.get_json())


if __name__ == '__main__':
    app.run(debug=True)
