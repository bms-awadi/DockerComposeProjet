from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import requests
import os

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "appdb"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppassword"),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
}

TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://tor:9050")
RANDOM_USER_API = "https://randomuser.me/api/"


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_proxies():
    return {"http": TOR_PROXY, "https": TOR_PROXY}


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(50),
            location VARCHAR(200),
            photo_url TEXT,
            source VARCHAR(20) DEFAULT 'manual',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()


@app.route("/api/health", methods=["GET"])
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()

        try:
            response = requests.get(
                "http://httpbin.org/ip", proxies=get_proxies(), timeout=5
            )
            tor_status = response.status_code == 200
            tor_ip = (
                response.json().get("origin", "unknown") if tor_status else "unknown"
            )
        except:
            tor_status = False
            tor_ip = "unknown"

        return jsonify(
            {
                "status": "healthy",
                "database": "connected",
                "postgres_version": version[0],
                "tor_connected": tor_status,
                "tor_ip": tor_ip,
            }
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "unhealthy", "database": "disconnected", "error": str(e)}
            ),
            500,
        )


@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, email, phone, location, photo_url, source, created_at 
            FROM users ORDER BY created_at DESC
        """
        )
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        users_list = []
        for user in users:
            users_list.append(
                {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "phone": user[3],
                    "location": user[4],
                    "photo_url": user[5],
                    "source": user[6],
                    "created_at": user[7].isoformat() if user[7] else None,
                }
            )

        return jsonify({"success": True, "users": users_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, email, phone, location, photo_url, source, created_at 
            FROM users WHERE id = %s
        """,
            (user_id,),
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify(
                {
                    "success": True,
                    "user": {
                        "id": user[0],
                        "username": user[1],
                        "email": user[2],
                        "phone": user[3],
                        "location": user[4],
                        "photo_url": user[5],
                        "source": user[6],
                        "created_at": user[7].isoformat() if user[7] else None,
                    },
                }
            )
        else:
            return jsonify({"success": False, "error": "User not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")

        if not username or not email:
            return (
                jsonify({"success": False, "error": "Username and email are required"}),
                400,
            )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, phone, location, photo_url, source) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id, created_at",
            (username, email, None, None, None, "manual"),
        )
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        return (
            jsonify(
                {
                    "success": True,
                    "user": {
                        "id": result[0],
                        "username": username,
                        "email": email,
                        "source": "manual",
                        "created_at": result[1].isoformat(),
                    },
                }
            ),
            201,
        )
    except psycopg2.IntegrityError:
        return jsonify({"success": False, "error": "Username already exists"}), 409
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")

        if not username or not email:
            return (
                jsonify({"success": False, "error": "Username and email are required"}),
                400,
            )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = %s, email = %s WHERE id = %s",
            (username, email, user_id),
        )

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": "User not found"}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(
            {
                "success": True,
                "user": {"id": user_id, "username": username, "email": email},
            }
        )
    except psycopg2.IntegrityError:
        return jsonify({"success": False, "error": "Username already exists"}), 409
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"success": False, "error": "User not found"}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/import-users", methods=["POST"])
def import_users():
    try:
        data = request.get_json()
        count = data.get("count", 10)

        if count > 50:
            count = 50

        response = requests.get(
            RANDOM_USER_API,
            params={"results": count},
            proxies=get_proxies(),
            timeout=30,
        )

        if response.status_code != 200:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Failed to fetch users from RandomUser API",
                    }
                ),
                500,
            )

        data = response.json()
        imported_users = []
        skipped = 0

        conn = get_db_connection()
        cursor = conn.cursor()

        for user_data in data.get("results", []):
            try:
                username = user_data["login"]["username"]
                email = user_data["email"]
                phone = user_data.get("phone", "")
                location = f"{user_data['location']['city']}, {user_data['location']['country']}"
                photo_url = user_data["picture"]["large"]

                cursor.execute(
                    """
                    INSERT INTO users (username, email, phone, location, photo_url, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """,
                    (username, email, phone, location, photo_url, "randomuser"),
                )

                user_id = cursor.fetchone()[0]
                imported_users.append(
                    {"id": user_id, "username": username, "email": email}
                )
                conn.commit()
            except psycopg2.IntegrityError:
                skipped += 1
                conn.rollback()
                continue

        cursor.close()
        conn.close()

        return jsonify(
            {
                "success": True,
                "imported": len(imported_users),
                "skipped": skipped,
                "users": imported_users,
                "via_tor": True,
            }
        )

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "error": f"Connection error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
