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
    if len(data['date_start']) == 8 and data['date_start'].isdigit():
        data['date_start'] = f"{data['date_start'][:4]}-{data['date_start'][4:6]}-{data['date_start'][6:]}"
    if len(data['date_end']) == 8 and data['date_end'].isdigit():
        data['date_end'] = f"{data['date_end'][:4]}-{data['date_end'][4:6]}-{data['date_end'][6:]}"   
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tours (country, city, name, price, date_start, date_end, description, seats, image)
            VALUES (:country, :city, :name, :price, :date_start, :date_end, :description, :seats, :image)
        """, data)
        conn.commit()

def update_tour_seats(tour_id, seats):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE tours SET seats = ? WHERE id = ?", (seats, tour_id))
        conn.commit()

def get_tour_by_id(tour_id):
    """Получить тур по ID"""
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tours WHERE id = ?", (tour_id,))
        return cur.fetchone()
    
    
def get_tour_by_id(tour_id):
    """
    Получает тур по его ID.
    
    Args:
        tour_id (int): ID тура.
    
    Returns:
        tuple | None: Кортеж с данными тура или None, если не найден.
    """
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tours WHERE id = ?", (tour_id,))
        return cur.fetchone()
    
def delete_tour(tour_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tours WHERE id = ?", (tour_id,))
        conn.commit()

def update_tour(data):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE tours SET
                country=?, city=?, name=?, price=?, date_start=?, date_end=?, description=?, seats=?
            WHERE id=?
        """, (data['country'], data['city'], data['name'], data['price'],
              data['date_start'], data['date_end'], data['description'], data['seats'], data['id']))
        conn.commit()