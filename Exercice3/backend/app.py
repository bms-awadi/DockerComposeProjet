from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://tor:9050")
API_URL = "https://randomuser.me/api/"


def get_proxies():
    return {"http": TOR_PROXY, "https": TOR_PROXY}


@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        response = requests.get(
            API_URL, params={"results": 10}, proxies=get_proxies(), timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            users = []

            for user in data.get("results", []):
                users.append(
                    {
                        "name": f"{user['name']['first']} {user['name']['last']}",
                        "photo": user["picture"]["large"],
                        "email": user.get("email", ""),
                        "location": f"{user['location']['city']}, {user['location']['country']}",
                        "phone": user.get("phone", ""),
                    }
                )

            return jsonify({"success": True, "users": users, "via_tor": True})
        else:
            return (
                jsonify({"success": False, "error": "Failed to fetch users from API"}),
                response.status_code,
            )

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Connection error: {str(e)}"}), 500


@app.route("/api/user", methods=["GET"])
def get_single_user():
    try:
        response = requests.get(API_URL, proxies=get_proxies(), timeout=30)

        if response.status_code == 200:
            data = response.json()
            user = data["results"][0]

            return jsonify(
                {
                    "success": True,
                    "user": {
                        "name": f"{user['name']['first']} {user['name']['last']}",
                        "photo": user["picture"]["large"],
                        "email": user.get("email", ""),
                        "location": f"{user['location']['city']}, {user['location']['country']}",
                        "phone": user.get("phone", ""),
                    },
                    "via_tor": True,
                }
            )
        else:
            return (
                jsonify({"success": False, "error": "Failed to fetch user from API"}),
                response.status_code,
            )

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Connection error: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    try:
        response = requests.get(
            "http://httpbin.org/ip", proxies=get_proxies(), timeout=10
        )

        if response.status_code == 200:
            ip_data = response.json()
            return jsonify(
                {
                    "status": "healthy",
                    "tor_connected": True,
                    "exit_ip": ip_data.get("origin", "unknown"),
                }
            )
        else:
            return jsonify({"status": "unhealthy", "tor_connected": False}), 500

    except Exception as e:
        return (
            jsonify({"status": "unhealthy", "tor_connected": False, "error": str(e)}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
