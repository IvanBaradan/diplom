from PyQt5.QtGui import QPixmap, QImage, QFont, QPainter, QColor
from PyQt5.QtCore import Qt
import random
import string

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
        return ''.join(random.choices(string.digits, k=4))
    
    @staticmethod
    def draw_captcha(text):
        width, height = 120, 50
        image = QImage(width, height, QImage.Format_RGB32)
        image.fill(QColor(255, 255, 255))
        
        painter = QPainter(image)
        font = QFont("Arial", 24)
        painter.setFont(font)
        
        for i, char in enumerate(text):
            x = 20 + i * 25
            y = random.randint(20, 30)
            angle = random.randint(-15, 15)
            
            painter.save()
            painter.translate(x, y)
            painter.rotate(angle)
            painter.setPen(QColor(
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(100, 255)
            ))
            painter.drawText(0, 0, char)
            painter.restore()
        
        for _ in range(100):
            x, y = random.randint(0, width), random.randint(0, height)
            painter.setPen(QColor(
                random.randint(150, 200),
                random.randint(150, 200),
                random.randint(150, 200)
            ))
            painter.drawPoint(x, y) 
        
        for _ in range(5):
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = random.randint(0, width), random.randint(0, height)
            painter.setPen(QColor(
                random.randint(150, 200),
                random.randint(150, 200),
                random.randint(150, 200)
            ))
            painter.drawLine(x1, y1, x2, y2)
        
        painter.end()
        
        return QPixmap.fromImage(image)