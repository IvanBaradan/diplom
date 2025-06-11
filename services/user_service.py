# services/user_service.py
import sqlite3
from database.db import get_db_path

def get_all_users():
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
