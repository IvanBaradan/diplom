# gui/auth.py

import tkinter as tk
from tkinter import ttk, messagebox
from services import auth_service
from gui import shared
import re

class AuthFrame(ttk.Frame):
    def __init__(self, master, on_login_success, theme_config, fonts):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.theme_config = theme_config
        self.fonts = fonts
        self.captcha_text = shared.generate_captcha_text()
        self.create_widgets()

    def create_widgets(self):
        self.pack(pady=50, expand=True)

        frame = ttk.Frame(self)
        frame.pack()

        ttk.Label(frame, text="Вход в систему", font=self.fonts['title'], foreground=self.theme_config['primary']).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(frame, text="Логин:", font=self.fonts['bold']).grid(row=1, column=0, sticky='e')
        self.username_entry = ttk.Entry(frame, font=self.fonts['normal'])
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Пароль:", font=self.fonts['bold']).grid(row=2, column=0, sticky='e')
        self.password_entry = ttk.Entry(frame, show='*', font=self.fonts['normal'])
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Капча:", font=self.fonts['bold']).grid(row=3, column=0, sticky='e')
        self.captcha_image = shared.draw_captcha(self.captcha_text)
        self.captcha_label = ttk.Label(frame, image=self.captcha_image)
        self.captcha_label.grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="Введите капчу:", font=self.fonts['bold']).grid(row=4, column=0, sticky='e')
        self.captcha_entry = ttk.Entry(frame, font=self.fonts['normal'])
        self.captcha_entry.grid(row=4, column=1, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Войти", command=self.login, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Регистрация", command=self.show_register_window, style='Secondary.TButton').pack(side=tk.LEFT, padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        captcha_input = self.captcha_entry.get()

        if captcha_input != self.captcha_text:
            messagebox.showerror("Ошибка", "Неверная капча")
            self.refresh_captcha()
            return

        user = auth_service.get_user_by_credentials(username, password)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.refresh_captcha()

    def refresh_captcha(self):
        self.captcha_text = shared.generate_captcha_text()
        self.captcha_image = shared.draw_captcha(self.captcha_text)
        self.captcha_label.config(image=self.captcha_image)
        self.captcha_entry.delete(0, tk.END)

    def show_register_window(self):
        RegisterWindow(self.master, self.refresh_captcha, self.theme_config, self.fonts)


class RegisterWindow(tk.Toplevel):
    def __init__(self, master, on_register, theme_config, fonts):
        super().__init__(master)
        self.title("Регистрация")
        self.on_register = on_register
        self.theme_config = theme_config
        self.fonts = fonts
        self.captcha_text = shared.generate_captcha_text()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20)

        ttk.Label(frame, text="Регистрация", font=self.fonts['title'],
                  foreground=self.theme_config['primary']).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields = [
            ("Логин", 'username'),
            ("Пароль", 'password'),
            ("ФИО", 'full_name'),
            ("Телефон", 'phone'),
        ]
        self.entries = {}

        for idx, (label, key) in enumerate(fields, start=1):
            ttk.Label(frame, text=f"{label}:", font=self.fonts['bold']).grid(row=idx, column=0, sticky='e', pady=5)

            if key == 'phone':
                self.phone_var = tk.StringVar()
                phone_entry = ttk.Entry(frame, textvariable=self.phone_var, font=self.fonts['normal'])
                phone_entry.grid(row=idx, column=1, pady=5)
                self.entries[key] = phone_entry
                self.phone_trace_id = self.phone_var.trace_add('write', self.on_phone_change)
            else:
                entry = ttk.Entry(frame, font=self.fonts['normal'], show='*' if key == 'password' else '')
                entry.grid(row=idx, column=1, pady=5)
                self.entries[key] = entry

        ttk.Label(frame, text="Капча:", font=self.fonts['bold']).grid(row=5, column=0, sticky='e')
        self.captcha_image = shared.draw_captcha(self.captcha_text)
        self.captcha_label = ttk.Label(frame, image=self.captcha_image)
        self.captcha_label.grid(row=5, column=1, pady=5)

        ttk.Label(frame, text="Введите капчу:", font=self.fonts['bold']).grid(row=6, column=0, sticky='e')
        self.captcha_entry = ttk.Entry(frame, font=self.fonts['normal'])
        self.captcha_entry.grid(row=6, column=1, pady=5)

        ttk.Button(frame, text="Зарегистрироваться", command=self.register_user,
                   style='Primary.TButton').grid(row=7, column=0, columnspan=2, pady=15)

    def on_phone_change(self, *args):
        raw = re.sub(r'\D', '', self.phone_var.get())

        if raw.startswith("8"):
            raw = "7" + raw[1:]

        if len(raw) > 11:
            raw = raw[:11]

        formatted = "+7 "
        if len(raw) >= 2:
            formatted += f"({raw[1:4]}"
        if len(raw) >= 4:
            formatted += f") {raw[4:7]}"
        if len(raw) >= 7:
            formatted += f"-{raw[7:9]}"
        if len(raw) >= 9:
            formatted += f"-{raw[9:11]}"

        # отключаем trace, чтобы избежать рекурсии
        self.phone_var.trace_remove("write", self.phone_trace_id)
        self.phone_var.set(formatted)
        self.phone_trace_id = self.phone_var.trace_add("write", self.on_phone_change)

    def register_user(self):
        username = self.entries['username'].get()
        password = self.entries['password'].get()
        full_name = self.entries['full_name'].get()
        phone = self.entries['phone'].get()
        captcha_input = self.captcha_entry.get()

        if captcha_input != self.captcha_text:
            messagebox.showerror("Ошибка", "Неверная капча")
            self.refresh_captcha()
            return

        if not all([username, password, full_name, phone]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        if auth_service.is_username_taken(username):
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
            return

        auth_service.register_user(username, password, full_name, phone)
        messagebox.showinfo("Успешно", "Регистрация завершена")
        self.destroy()
        self.on_register()

    def refresh_captcha(self):
        self.captcha_text = shared.generate_captcha_text()
        self.captcha_image = shared.draw_captcha(self.captcha_text)
        self.captcha_label.config(image=self.captcha_image)
        self.captcha_entry.delete(0, tk.END)