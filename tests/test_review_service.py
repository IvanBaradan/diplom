# tests/test_review_service.py
import sqlite3
from datetime import datetime, timedelta
from database.db import get_db_path

def add_test_reviews():
    # Подключаемся к базе данных
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    try:
        # Сначала добавляем тестовых пользователей и туры, если их нет
        cursor.execute("INSERT OR IGNORE INTO users (username, password, full_name, phone, role) VALUES ('test_user1', 'pass1', 'Тестовый Пользователь 1', '+79111111111', 'user')")
        cursor.execute("INSERT OR IGNORE INTO users (username, password, full_name, phone, role) VALUES ('test_user2', 'pass2', 'Тестовый Пользователь 2', '+79222222222', 'user')")
        
        cursor.execute("INSERT OR IGNORE INTO tours (country, city, name, price, date_start, date_end, description, seats) VALUES ('Россия', 'Сочи', 'Тестовый тур 1', 30000, '2024-01-01', '2024-01-07', 'Описание тестового тура 1', 10)")
        cursor.execute("INSERT OR IGNORE INTO tours (country, city, name, price, date_start, date_end, description, seats) VALUES ('Россия', 'Калининград', 'Тестовый тур 2', 25000, '2024-02-01', '2024-02-07', 'Описание тестового тура 2', 8)")
        
        conn.commit()

        # Получаем ID добавленных записей
        user1_id = cursor.execute("SELECT id FROM users WHERE username = 'test_user1'").fetchone()[0]
        user2_id = cursor.execute("SELECT id FROM users WHERE username = 'test_user2'").fetchone()[0]
        tour1_id = cursor.execute("SELECT id FROM tours WHERE name = 'Тестовый тур 1'").fetchone()[0]
        tour2_id = cursor.execute("SELECT id FROM tours WHERE name = 'Тестовый тур 2'").fetchone()[0]

        # Тестовые отзывы (user_id, tour_id, rating, comment, booking_date)
        test_reviews = [
            (user1_id, tour1_id, 5, 'Отличный тур! Все понравилось.', datetime.now() - timedelta(days=10)),
            (user1_id, tour2_id, 4, 'Хороший отель, но далеко от моря.', datetime.now() - timedelta(days=20)),
            (user2_id, tour1_id, 3, 'Нормально, но питание могло быть лучше.', datetime.now() - timedelta(days=15)),
            (user2_id, tour2_id, 5, 'Прекрасный отдых, рекомендую!', datetime.now() - timedelta(days=5))
        ]

        # Добавляем отзывы
        for user_id, tour_id, rating, comment, booking_date in test_reviews:
            cursor.execute(
                """INSERT INTO orders (user_id, tour_id, booking_date, rating, comment, status) 
                VALUES (?, ?, ?, ?, ?, 'purchased')""",
                (user_id, tour_id, booking_date.strftime('%Y-%m-%d %H:%M:%S'), rating, comment)
            )

        conn.commit()
        print(f"Успешно добавлено {len(test_reviews)} тестовых отзыва")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении тестовых отзывов: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    add_test_reviews()