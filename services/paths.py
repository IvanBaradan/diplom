# services/paths.py
import os
import sys

def get_receipts_dir():
    """Возвращает путь к папке с чеками с учетом режима exe"""
    if getattr(sys, 'frozen', False):
        # Режим exe - сохраняем рядом с программой
        base_dir = os.path.dirname(sys.executable)
    else:
        # Режим разработки - в папке проекта
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    receipts_dir = os.path.join(base_dir, 'receipts')
    os.makedirs(receipts_dir, exist_ok=True)
    return receipts_dir