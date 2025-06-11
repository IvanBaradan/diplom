# gui/shared.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import io

class Theme:
    def __init__(self):
        self.light_theme = {
            'bg': '#f5f6f7',
            'card': '#ffffff',
            'text': '#333333',
            'primary': '#00bae5',
            'secondary': '#ff6d00'
        }
        self.dark_theme = {
            'bg': '#2d2d2d',
            'card': '#3d3d3d',
            'text': '#ffffff',
            'primary': '#0088a3',
            'secondary': '#cc5500'
        }
        self.current = self.light_theme
    
    def toggle_theme(self):
        self.current = self.dark_theme if self.current == self.light_theme else self.light_theme
        return self.current

class CaptchaGenerator:
    @staticmethod
    def generate_text():
        return ''.join(random.choice('0123456789') for _ in range(4))
    
    @staticmethod
    def draw_captcha(text):
        width, height = 120, 50
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            
        for i, char in enumerate(text):
            x = 20 + i * 25
            y = random.randint(5, 15)
            angle = random.randint(-15, 15)
            
            char_img = Image.new('RGBA', (30, 30), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((0, 0), char, font=font, 
                          fill=(random.randint(0, 100), random.randint(0, 100), random.randint(100, 255)))
            char_img = char_img.rotate(angle, expand=1)
            image.paste(char_img, (x, y), char_img)
            
        for _ in range(100):
            x, y = random.randint(0, width), random.randint(0, height)
            draw.point((x, y), fill=(random.randint(150, 200), random.randint(150, 200), random.randint(150, 200)))
            
        for _ in range(5):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=(random.randint(150, 200), random.randint(150, 200), random.randint(150, 200)), width=1)
            
        return ImageTk.PhotoImage(image)