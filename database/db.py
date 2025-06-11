# database/db.py
import sqlite3
import os

DB_PATH = 'tour_agency.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    db_exists = os.path.exists(DB_PATH)
    conn = get_connection()
    cur = conn.cursor()

    # Таблица пользователей
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
        )
    """)

    # Таблица туров
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            date_start TEXT NOT NULL,
            date_end TEXT NOT NULL,
            description TEXT,
            seats INTEGER NOT NULL,
            image BLOB
        )
    """)

    # Таблица заказов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tour_id INTEGER NOT NULL,
            booking_date TEXT,
            rating TEXT,
            comment TEXT,
            status TEXT NOT NULL CHECK(status IN ('booked', 'purchased', 'cancelled', 'refund_requested')),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(tour_id) REFERENCES tours(id)
        )
    """)

    # Создание администратора по умолчанию
    cur.execute("SELECT 1 FROM users WHERE username = 'admin'")
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO users (username, password, full_name, phone, role)
            VALUES ('admin', 'admin', 'Администратор', '+79999999999', 'admin')
        """)

    conn.commit()
    conn.close()
