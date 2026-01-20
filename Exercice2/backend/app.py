from flask import Flask, request, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app)

database.init_db()


@app.route("/api/users", methods=["GET"])
def get_users():
    users = database.get_all_users()
    return jsonify(users)


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = database.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user_id = database.create_user(username, password)
    if user_id:
        return jsonify({"id": user_id, "username": username}), 201
    return jsonify({"error": "Username already exists"}), 409


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if database.update_user(user_id, username, password):
        return jsonify({"id": user_id, "username": username})
    return jsonify({"error": "User not found or username exists"}), 404


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if database.delete_user(user_id):
        return jsonify({"message": "User deleted"})
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
