from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

def generate_pdf_receipt(order_id, tour_name, username, price, save_path=None):
    if not save_path:
        receipts_dir = os.path.join(os.getcwd(), "receipts")
        os.makedirs(receipts_dir, exist_ok=True)
        save_path = os.path.join(receipts_dir, f"receipt_{order_id}.pdf")

    # Путь к TTF-файлу
    font_path = os.path.join(os.getcwd(), "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("Файл DejaVuSans.ttf не найден. Положи его рядом с pdf_generator.py")

    # Регистрация шрифта
    pdfmetrics.registerFont(TTFont("DejaVu", font_path))

    c = canvas.Canvas(save_path, pagesize=A4)
    c.setFont("DejaVu", 14)

    y = 800
    lines = [
        "Чек покупки тура",
        f"Номер заказа: {order_id}",
        f"Пользователь: {username}",
        f"Тур: {tour_name}",
        f"Цена: {price} руб.",
        f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    for line in lines:
        c.drawString(100, y, line)
        y -= 25

    c.save()
    return save_path
