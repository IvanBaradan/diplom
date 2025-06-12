# services/review_service.py
import sqlite3
from database.db import get_db_path

def add_review(order_id, rating, comment):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders SET rating = ?, comment = ?
            WHERE id = ?
        """, (rating, comment, order_id))
        conn.commit()

def get_reviews_by_tour(tour_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT rating, comment FROM orders WHERE tour_id = ? AND rating IS NOT NULL", (tour_id,))
        return cur.fetchall()

def calculate_average_rating(tour_id):
    reviews = get_reviews_by_tour(tour_id)
    if not reviews:
        return None
    ratings = [int(r[0]) for r in reviews if r[0].isdigit()]
    return round(sum(ratings) / len(ratings), 2) if ratings else None

    
def add_review(order_id, rating, comment):
    """Добавить отзыв в заказ"""
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE orders SET rating=?, comment=? WHERE id=?", (rating, comment, order_id))
        conn.commit()


def get_reviews_for_tour(tour_id):
    """Отзывы для тура"""
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT o.rating, o.comment, u.full_name 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            WHERE o.tour_id=? AND o.rating IS NOT NULL
        """, (tour_id,))
        return cur.fetchall()


def get_average_rating(tour_id):
    """Средний рейтинг тура"""
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT AVG(rating) FROM orders WHERE tour_id=? AND rating IS NOT NULL", (tour_id,))
        result = cur.fetchone()[0]
        return round(result, 1) if result else None
