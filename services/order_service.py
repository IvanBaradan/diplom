# services/order_service.py
import sqlite3
from datetime import datetime
from database.db import get_db_path

def book_tour(user_id, tour_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO orders (user_id, tour_id, booking_date, status)
            VALUES (?, ?, ?, 'booked')
        """, (user_id, tour_id, booking_date))
        cur.execute("UPDATE tours SET seats = seats - 1 WHERE id = ?", (tour_id,))
        conn.commit()

def purchase_tour(user_id, tour_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Вставляем заказ и возвращаем ID
        cur.execute("""
            INSERT INTO orders (user_id, tour_id, booking_date, status)
            VALUES (?, ?, ?, 'purchased')
        """, (user_id, tour_id, purchase_date))
        
        # Обновляем количество мест
        cur.execute("UPDATE tours SET seats = seats - 1 WHERE id = ?", (tour_id,))
        
        # Получаем ID созданного заказа
        order_id = cur.lastrowid
        conn.commit()
        return order_id

    
    
def request_refund(order_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'refund_requested' WHERE id = ?", (order_id,))
        conn.commit()

def get_orders_by_user(user_id):
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
        return cur.fetchall()
    
    
def get_orders_by_user_and_status(user_id, statuses):
    """Получить заказы пользователя с определёнными статусами"""
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        placeholders = ','.join('?' * len(statuses))
        cur.execute(f"""
            SELECT * FROM orders WHERE user_id = ? AND status IN ({placeholders})
        """, (user_id, *statuses))
        return cur.fetchall()


def approve_refund(order_id):
    """Одобрить возврат: удаляет заказ и возвращает место"""
    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT tour_id FROM orders WHERE id=?", (order_id,))
        tour_id = cur.fetchone()[0]
        cur.execute("DELETE FROM orders WHERE id=?", (order_id,))
        cur.execute("UPDATE tours SET seats = seats + 1 WHERE id=?", (tour_id,))
        conn.commit()
