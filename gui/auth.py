from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from services.auth_service import get_user_by_credentials, register_user, is_username_taken
from gui.shared import CaptchaGenerator

class AuthFrame(QWidget):
    def __init__(self, on_login_success, switch_to_register):
        super().__init__()
        self.on_login_success = on_login_success
        self.switch_to_register = switch_to_register
        self.captcha = CaptchaGenerator()
        self.captcha_text = self.captcha.generate_text()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Вход в систему")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        # Капча
        self.captcha_label = QLabel()
        self.update_captcha()
        layout.addWidget(self.captcha_label, alignment=Qt.AlignCenter)
        
        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("Введите капчу")
        layout.addWidget(self.captcha_input)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self.login)
        btn_layout.addWidget(login_btn)
        
        register_btn = QPushButton("Регистрация")
        register_btn.clicked.connect(self.switch_to_register)
        btn_layout.addWidget(register_btn)
        
        layout.addLayout(btn_layout)
    
    def update_captcha(self):
        pixmap = self.captcha.draw_captcha(self.captcha_text)
        self.captcha_label.setPixmap(pixmap)
    
    def login(self):
        username = self.login_input.text()
        password = self.password_input.text()
        captcha = self.captcha_input.text()
        
        if captcha != self.captcha_text:
            QMessageBox.critical(self, "Ошибка", "Неверная капча")
            self.refresh_captcha()
            return
            
        user = get_user_by_credentials(username, password)
        if user:
            self.on_login_success(user)
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")
            self.refresh_captcha()
    
    def refresh_captcha(self):
        self.captcha_text = self.captcha.generate_text()
        self.update_captcha()
        self.captcha_input.clear()

class RegisterFrame(QWidget):
    def __init__(self, on_back, on_register_success):
        super().__init__()
        self.on_back = on_back
        self.on_register_success = on_register_success
        self.captcha = CaptchaGenerator()
        self.captcha_text = self.captcha.generate_text()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Регистрация")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("ФИО")
        layout.addWidget(self.fullname_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        layout.addWidget(self.phone_input)
        
        # Капча
        self.captcha_label = QLabel()
        self.update_captcha()
        layout.addWidget(self.captcha_label, alignment=Qt.AlignCenter)
        
        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("Введите капчу")
        layout.addWidget(self.captcha_input)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self.register)
        btn_layout.addWidget(register_btn)
        
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.on_back)
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
    
    def update_captcha(self):
        pixmap = self.captcha.draw_captcha(self.captcha_text)
        self.captcha_label.setPixmap(pixmap)
    
    def register(self):
        if not self.validate_fields():
            return
            
        if is_username_taken(self.username_input.text()):
            QMessageBox.critical(self, "Ошибка", "Логин уже занят")
            return
            
        register_user(
            self.username_input.text(),
            self.password_input.text(),
            self.fullname_input.text(),
            self.phone_input.text()
        )
        QMessageBox.information(self, "Успех", "Регистрация завершена")
        self.on_register_success()
    
    def validate_fields(self):
        # Проверка всех обязательных полей
        if not all([
            self.username_input.text(),
            self.password_input.text(),
            self.fullname_input.text(),
            self.captcha_input.text() == self.captcha_text
        ]):
            QMessageBox.critical(self, "Ошибка", "Заполните все поля и правильно введите капчу")
            return False
        return True