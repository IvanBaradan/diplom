# services/pdf_generator.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='receipts.log'
)

def get_base_dir():
    """Возвращает базовую директорию (рядом с .exe или в dev)"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    return os.getcwd()

def register_fonts():
    try:
        base_dir = get_base_dir()
        font_path = os.path.join(base_dir, 'fonts', 'DejaVuSans.ttf')
        pdfmetrics.registerFont(TTFont('DejaVu', font_path))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', font_path))
        return True
    except Exception as e:
        logging.error(f"Ошибка регистрации шрифтов: {e}")
        return False

def generate_pdf_receipt(order_id, tour_name, username, price):
    try:
        if not register_fonts():
            raise Exception("Не удалось загрузить шрифты")

        base_dir = get_base_dir()
        receipts_dir = os.path.join(base_dir, 'receipts')
        os.makedirs(receipts_dir, exist_ok=True)

        filename = f"receipt_{order_id}.pdf"
        filepath = os.path.join(receipts_dir, filename)

        c = canvas.Canvas(filepath, pagesize=A4)

        c.setFont("DejaVu-Bold", 16)
        c.drawString(100, 800, "Турагентство 'Путешествия'")

        c.setFont("DejaVu", 14)
        y_position = 770
        lines = [
            f"Чек №: {order_id}",
            f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            "",
            f"Клиент: {username}",
            f"Тур: {tour_name}",
            f"Сумма: {price} руб."
        ]
        for line in lines:
            c.drawString(100, y_position, line)
            y_position -= 25

        c.setFont("DejaVu", 12)
        c.drawString(100, y_position - 40, "Спасибо за покупку!")

        c.save()
        logging.info(f"Чек создан: {filepath}")
        return filepath

    except Exception as e:
        logging.error(f"Ошибка создания чека: {e}")
        return None
