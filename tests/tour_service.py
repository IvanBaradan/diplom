import sqlite3
from database.db import get_db_path

def insert_sample_tours():
    from datetime import date, timedelta
    today = date.today()
    base_data = [
        # Базы отдыха
        ("Россия", "Карелия", "База отдыха «Лесная сказка»", 32000, today, today + timedelta(days=7), "Живописная природа, баня, рыбалка", 10, None),
        ("Россия", "Астрахань", "База отдыха «Волжская гавань»", 28000, today, today + timedelta(days=5), "Рыбалка и барбекю", 8, None),
        ("Россия", "Башкирия", "Эко-база «Танып»", 35000, today, today + timedelta(days=6), "Сосновый лес, домики, баня", 12, None),
        ("Россия", "Алтай", "Усадьба на берегу Катуни", 40000, today, today + timedelta(days=8), "Тишина, горы, река", 5, None),
        ("Россия", "Тверь", "База отдыха «Лесной уют»", 30000, today, today + timedelta(days=5), "Природа и покой", 7, None),

        # Санатории
        ("Россия", "Кисловодск", "Санаторий «Целебный источник»", 45000, today, today + timedelta(days=10), "Минеральные воды и лечение", 15, None),
        ("Россия", "Сочи", "Санаторий «Южный берег»", 48000, today, today + timedelta(days=12), "Терапия и море", 10, None),
        ("Россия", "Ессентуки", "Санаторий «Здоровье»", 43000, today, today + timedelta(days=9), "Лечение и релакс", 14, None),
        ("Россия", "Белокуриха", "Санаторий «Алтайский ключ»", 47000, today, today + timedelta(days=10), "Горный климат, процедуры", 9, None),
        ("Россия", "Пятигорск", "Санаторий «Минеральный мир»", 42000, today, today + timedelta(days=8), "Радоновые ванны", 13, None),

        # Лыжные курорты
        ("Россия", "Сочи", "Красная Поляна", 60000, today, today + timedelta(days=7), "Сноуборд, трассы, горы", 10, None),
        ("Россия", "Шерегеш", "Шерегеш Курорт", 55000, today, today + timedelta(days=6), "Пудра и подъёмники", 8, None),
        ("Россия", "Эльбрус", "Гора Эльбрус", 58000, today, today + timedelta(days=7), "Высокие трассы, виды", 7, None),
        ("Россия", "Северная Осетия", "Куртатинское ущелье", 53000, today, today + timedelta(days=5), "Катание в горах", 6, None),
        ("Россия", "Кемерово", "Курорт Танай", 49000, today, today + timedelta(days=4), "Семейный отдых и лыжи", 9, None),
    ]

    with sqlite3.connect(get_db_path()) as conn:
        cur = conn.cursor()
        cur.executemany("""
            INSERT INTO tours (country, city, name, price, date_start, date_end, description, seats, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, base_data)
        conn.commit()
        
if __name__ == "__main__":
    insert_sample_tours()

# run as: python -m tests.tour_service
