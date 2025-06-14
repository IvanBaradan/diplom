# tests/test_user_service.py
import sqlite3
from database.db import get_db_path

def add_test_users():
    # Тестовые пользователи
    test_users = [
        ('user1', 'password1', 'Иван Иванов', '+79111111111', 'user'),
        ('user2', 'password2', 'Петр Петров', '+79222222222', 'user'),
        ('manager', 'manager123', 'Анна Сидорова', '+79333333333', 'admin'),
        ('client1', 'clientpass', 'Ольга Кузнецова', '+79444444444', 'user'),
        ('client2', 'clientpass', 'Сергей Смирнов', '+79555555555', 'user')
    ]

    # Подключаемся к базе данных
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    try:
        # Добавляем пользователей
        for username, password, full_name, phone, role in test_users:
            cursor.execute(
                "INSERT INTO users (username, password, full_name, phone, role) VALUES (?, ?, ?, ?, ?)",
                (username, password, full_name, phone, role)
            )
        
        # Сохраняем изменения
        conn.commit()
        print("Успешно добавлено 5 тестовых пользователей")
        
    except sqlite3.IntegrityError as e:
        print(f"Ошибка: {e}. Возможно, некоторые пользователи уже существуют.")
    finally:
        # Закрываем соединение
        conn.close()

if __name__ == '__main__':
    add_test_users()