# services/tour_service.py
import sqlite3
from database.db import get_db_path

def get_all_tours():
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tours")
        return cur.fetchall()

def get_available_tours():
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tours WHERE seats > 0")
        return cur.fetchall()

def add_tour(data):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tours (country, city, name, price, date_start, date_end, description, seats, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()

def update_tour_seats(tour_id, seats):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE tours SET seats = ? WHERE id = ?", (seats, tour_id))
        conn.commit()

def get_tour_by_id(tour_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tours WHERE id = ?", (tour_id,))
        return cur.fetchone()
