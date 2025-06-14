# services/auth_service.py

import sqlite3
import bcrypt
from database.db import get_db_path


def get_user_by_credentials(username, password):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return {
                'id': user[0],
                'username': user[1],
                'full_name': user[3],
                'phone': user[4],
                'role': user[5]
            }
        return None

def register_user(username, password, full_name, phone):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, full_name, phone, role) VALUES (?, ?, ?, ?, ?)",
                    (username, hashed.decode('utf-8'), full_name, phone, 'user'))
        conn.commit()


def is_username_taken(username):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cur.fetchone() is not None

def delete_user(user_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()