# services/validators.py

import re
from datetime import datetime


def format_date_input(text: str) -> str:
    """Автоматически форматирует дату YYYYMMDD → YYYY-MM-DD"""
    if len(text) == 8 and text.isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:]}"
    return text


def format_phone_input(text: str) -> str:
    """Форматирует номер телефона в +7 (XXX) XXX-XX-XX"""
    digits = re.sub(r'\D', '', text)
    if len(digits) == 11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    if len(digits) == 11:
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    return text


def is_valid_date(date_text: str) -> bool:
    """Проверка даты на формат YYYY-MM-DD"""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_phone(phone: str) -> bool:
    """Проверка телефона по шаблону +7 (XXX) XXX-XX-XX"""
    return bool(re.match(r"\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}", phone))


def is_non_empty(*fields) -> bool:
    """Проверка, что все поля непустые"""
    return all(field.strip() != '' for field in fields)
