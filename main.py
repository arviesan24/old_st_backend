from flask import Flask, jsonify
from blueprints.users import blueprint as user_blueprint


app = Flask(__name__)
app.register_blueprint(user_blueprint)


@app.route("/")
def main():
    return jsonify({
        'status': 'OK'
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
