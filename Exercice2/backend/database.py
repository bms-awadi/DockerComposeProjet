import sqlite3
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/data/users.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def create_user(username, password):
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def get_all_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, username FROM users").fetchall()
    conn.close()
    return [dict(user) for user in users]


def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, username FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user(user_id, username, password):
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE users SET username = ?, password = ? WHERE id = ?",
            (username, password, user_id),
        )
        conn.commit()
        affected = conn.total_changes
        conn.close()
        return affected > 0
    except sqlite3.IntegrityError:
        conn.close()
        return False


def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    affected = conn.total_changes
    conn.close()
    return affected > 0
