# gui/shared.py

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
import random
import json
import os
import sqlite3
from colorsys import rgb_to_hls, hls_to_rgb
from database.db import get_connection


# ===================== ТЕМА И СТИЛИ =====================
def setup_fonts():
    return {
        'title': tkfont.Font(family='Segoe UI', size=24, weight='bold'),
        'subtitle': tkfont.Font(family='Segoe UI', size=16),
        'normal': tkfont.Font(family='Segoe UI', size=12),
        'bold': tkfont.Font(family='Segoe UI', size=12, weight='bold'),
        'small': tkfont.Font(family='Segoe UI', size=10)
    }


def setup_theme(style: ttk.Style, fonts: dict, dark_mode=False, color_scheme=None):
    """Устанавливает тему оформления и цветовую палитру"""

    if dark_mode:
        bg_color = "#2d2d2d"
        card_color = "#3d3d3d"
        text_color = "#ffffff"
        border_color = "#555555"
        header_color = "#1e1e1e"
        entry_bg = "#3d3d3d"
        entry_fg = "#ffffff"
        select_bg = "#555555"
        select_fg = "#ffffff"
    else:
        bg_color = "#f5f6f7"
        card_color = "#ffffff"
        text_color = "#333333"
        border_color = "#e0e0e0"
        header_color = "#263238"
        entry_bg = "#ffffff"
        entry_fg = "#333333"
        select_bg = "#e0e0e0"
        select_fg = "#333333"

    # Цветовая схема
    if color_scheme:
        primary_color = color_scheme['primary']
        secondary_color = color_scheme['secondary']
        accent_color = color_scheme['accent']
    else:
        primary_color = "#00bae5"
        secondary_color = "#ff6d00"
        accent_color = "#5c6bc0"

    success_color = "#4caf50"
    danger_color = "#f44336"
    warning_color = "#ff9800"

    # Общие стили
    style.theme_use('clam')
    style.configure('.', background=bg_color, foreground=text_color)

    style.configure('TFrame', background=bg_color)
    style.configure('Card.TFrame', background=card_color, relief="raised", borderwidth=1)
    style.configure('TLabel', background=bg_color, foreground=text_color, font=fonts['normal'])

    style.configure('Title.TLabel', font=fonts['title'], foreground=primary_color)
    style.configure('Subtitle.TLabel', font=fonts['subtitle'], foreground=text_color)

    style.configure('TButton', font=fonts['bold'], padding=8, relief="flat", background=card_color, foreground=text_color)

    style.configure('Primary.TButton', background=primary_color, foreground='white')
    style.configure('Secondary.TButton', background=secondary_color, foreground='white')
    style.configure('Success.TButton', background=success_color, foreground='white')
    style.configure('Danger.TButton', background=danger_color, foreground='white')
    style.configure('Warning.TButton', background=warning_color, foreground='white')

    style.configure('TEntry',
                    fieldbackground=entry_bg, foreground=entry_fg,
                    background=entry_bg, insertcolor=entry_fg,
                    bordercolor=border_color)

    style.configure('TCombobox',
                    fieldbackground=entry_bg, background=entry_bg,
                    foreground=entry_fg)

    style.configure('Treeview',
                    background=entry_bg,
                    fieldbackground=entry_bg,
                    foreground=entry_fg,
                    rowheight=30,
                    font=fonts['normal'])

    style.configure('Treeview.Heading',
                    background=primary_color,
                    foreground='white',
                    font=fonts['bold'])

    style.configure('TLabelframe', background=bg_color, foreground=text_color)
    style.configure('TLabelframe.Label', background=bg_color, foreground=text_color)

    return {
        'bg': bg_color,
        'card': card_color,
        'text': text_color,
        'primary': primary_color,
        'secondary': secondary_color,
        'accent': accent_color,
        'success': success_color,
        'danger': danger_color,
        'warning': warning_color,
        'header': header_color,
        'entry_bg': entry_bg,
        'entry_fg': entry_fg
    }

# ===================== КАПЧА =====================

def generate_captcha_text(length=4) -> str:
    """Генерирует текст капчи"""
    return ''.join(random.choices('0123456789', k=length))


def draw_captcha(captcha_text: str) -> ImageTk.PhotoImage:
    """Рисует изображение капчи"""
    width, height = 120, 50
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    for i, char in enumerate(captcha_text):
        x = 20 + i * 25
        y = random.randint(5, 15)
        angle = random.randint(-15, 15)

        temp_img = Image.new('RGBA', (30, 30), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((0, 0), char, font=font, fill=(
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(100, 255)
        ))

        temp_img = temp_img.rotate(angle, expand=1)
        image.paste(temp_img, (x, y), temp_img)

    for _ in range(100):
        draw.point((random.randint(0, width), random.randint(0, height)),
                   fill=(random.randint(150, 200), random.randint(150, 200), random.randint(150, 200)))

    for _ in range(3):
        draw.line((random.randint(0, width), random.randint(0, height),
                   random.randint(0, width), random.randint(0, height)),
                  fill=(random.randint(150, 200), random.randint(150, 200), random.randint(150, 200)),
                  width=1)

    return ImageTk.PhotoImage(image)

# ===================== ТЕМА (цветовая логика) =====================

def lighten_color(color: str, amount=0.2) -> str:
    """Осветляет цвет"""
    rgb = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    h, l, s = rgb_to_hls(*[x / 255.0 for x in rgb])
    l = min(1.0, l + amount)
    new_rgb = hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in new_rgb)


def darken_color(color: str, amount=0.2) -> str:
    """Затемняет цвет"""
    rgb = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    h, l, s = rgb_to_hls(*[x / 255.0 for x in rgb])
    l = max(0.0, l - amount)
    new_rgb = hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % tuple(int(x * 255) for x in new_rgb)
