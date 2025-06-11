# services/review_service.py
import sqlite3

DB_PATH = 'tour_agency.db'

def add_review(order_id, rating, comment):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders SET rating = ?, comment = ?
            WHERE id = ?
        """, (rating, comment, order_id))
        conn.commit()

def get_reviews_by_tour(tour_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT rating, comment FROM orders WHERE tour_id = ? AND rating IS NOT NULL", (tour_id,))
        return cur.fetchall()

def calculate_average_rating(tour_id):
    reviews = get_reviews_by_tour(tour_id)
    if not reviews:
        return None
    ratings = [int(r[0]) for r in reviews if r[0].isdigit()]
    return round(sum(ratings) / len(ratings), 2) if ratings else None
