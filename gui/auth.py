# gui/auth.py
import tkinter as tk
from tkinter import ttk, messagebox
from .shared import Theme, CaptchaGenerator
from services.auth_service import get_user_by_credentials, register_user, is_username_taken

class AuthFrame(ttk.Frame):
    def __init__(self, parent, on_login_success, switch_to_register):
        super().__init__(parent)
        self.theme = Theme()
        self.captcha = CaptchaGenerator()
        self.on_login_success = on_login_success
        self.switch_to_register = switch_to_register
        self.captcha_text = self.captcha.generate_text()
        self.create_widgets()
        
    def create_widgets(self):
        self.login_label = ttk.Label(self, text="Вход в систему", style='Title.TLabel')
        self.login_label.pack(pady=20)
        
        self.login_entry = ttk.Entry(self)
        self.login_entry.pack(pady=5, fill=tk.X, padx=20)
        self.login_entry.insert(0, "Логин")
        
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5, fill=tk.X, padx=20)
        self.password_entry.insert(0, "Пароль")
        
        self.captcha_image = self.captcha.draw_captcha(self.captcha_text)
        self.captcha_label = ttk.Label(self, image=self.captcha_image)
        self.captcha_label.pack(pady=5)
        
        self.captcha_entry = ttk.Entry(self)
        self.captcha_entry.pack(pady=5, fill=tk.X, padx=20)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.login_btn = ttk.Button(btn_frame, text="Войти", command=self.login, style='Primary.TButton')
        self.login_btn.pack(side=tk.LEFT, expand=True)
        
        self.register_btn = ttk.Button(btn_frame, text="Регистрация", 
                                      command=self.switch_to_register, style='Secondary.TButton')
        self.register_btn.pack(side=tk.LEFT, expand=True, padx=5)
    
    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        captcha = self.captcha_entry.get()
        
        if captcha != self.captcha_text:
            messagebox.showerror("Ошибка", "Неверная капча")
            self.refresh_captcha()
            return
            
        user = get_user_by_credentials(username, password)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.refresh_captcha()
            
    def refresh_captcha(self):
        self.captcha_text = self.captcha.generate_text()
        self.captcha_image = self.captcha.draw_captcha(self.captcha_text)
        self.captcha_label.config(image=self.captcha_image)
        self.captcha_entry.delete(0, tk.END)

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, on_back, on_register_success):
        super().__init__(parent)
        self.theme = Theme()
        self.captcha = CaptchaGenerator()
        self.on_back = on_back
        self.on_register_success = on_register_success
        self.captcha_text = self.captcha.generate_text()
        self.create_widgets()
        
    def create_widgets(self):
        self.reg_label = ttk.Label(self, text="Регистрация", style='Title.TLabel')
        self.reg_label.pack(pady=20)

        # Логин
        ttk.Label(self, text="Логин").pack(pady=2)
        self.login_entry = ttk.Entry(self)
        self.login_entry.pack(pady=2, fill=tk.X, padx=20)

        # Пароль
        ttk.Label(self, text="Пароль").pack(pady=2)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=2, fill=tk.X, padx=20)

        # ФИО
        ttk.Label(self, text="ФИО").pack(pady=2)
        self.fullname_entry = ttk.Entry(self)
        self.fullname_entry.pack(pady=2, fill=tk.X, padx=20)

        # Телефон
        ttk.Label(self, text="Телефон").pack(pady=2)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.pack(pady=2, fill=tk.X, padx=20)

        # Капча
        self.captcha_image = self.captcha.draw_captcha(self.captcha_text)
        self.captcha_label = ttk.Label(self, image=self.captcha_image)
        self.captcha_label.pack(pady=5)

        self.captcha_entry = ttk.Entry(self)
        self.captcha_entry.pack(pady=5, fill=tk.X, padx=20)

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10, fill=tk.X, padx=20)

        self.register_btn = ttk.Button(btn_frame, text="Зарегистрироваться",
                                    command=self.register, style='Primary.TButton')
        self.register_btn.pack(side=tk.LEFT, expand=True)

        self.back_btn = ttk.Button(btn_frame, text="Назад",
                                command=self.on_back, style='Secondary.TButton')
        self.back_btn.pack(side=tk.LEFT, expand=True, padx=5)

    
    def register(self):
        if not self.validate_fields():
            return
            
        if is_username_taken(self.login_entry.get()):
            messagebox.showerror("Ошибка", "Логин уже занят")
            return
            
        register_user(
            self.login_entry.get(),
            self.password_entry.get(),
            self.fullname_entry.get(),
            self.phone_entry.get()
        )
        messagebox.showinfo("Успех", "Регистрация завершена")
        self.on_register_success()
        
    def validate_fields(self):
        # Добавьте проверку всех полей
        return True