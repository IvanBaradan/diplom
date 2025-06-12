# services/pdf_generator.py

from fpdf import FPDF
from datetime import datetime
import os

def generate_pdf_receipt(order_id, tour_name, username, price, save_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Чек на покупку тура", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Номер заказа: {order_id}", ln=True)
    pdf.cell(200, 10, txt=f"Пользователь: {username}", ln=True)
    pdf.cell(200, 10, txt=f"Название тура: {tour_name}", ln=True)
    pdf.cell(200, 10, txt=f"Цена: {price} руб.", ln=True)
    pdf.cell(200, 10, txt=f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    if not save_path:
        receipt_dir = os.path.join(os.getcwd(), "receipts")
        os.makedirs(receipt_dir, exist_ok=True)
        save_path = os.path.join(receipt_dir, f"receipt_{order_id}.pdf")

    pdf.output(save_path)
    return save_path
