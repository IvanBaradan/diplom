# gui/app.py

import tkinter as tk
from tkinter import ttk
from gui.auth import AuthFrame
from gui.user import UserMenu
from gui.admin import AdminMenu
from gui import shared


class TourAgencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Турагентство")
        self.root.geometry("1200x800")

        self.fonts = shared.setup_fonts()
        self.style = ttk.Style()
        self.theme_config = shared.setup_theme(self.style, self.fonts, dark_mode=False)

        self.current_user = None
        self.current_frame = None

        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login(self):
        self.clear_frame()
        self.current_frame = AuthFrame(self.root, self.on_login_success, self.theme_config, self.fonts)

    def on_login_success(self, user):
        self.current_user = user
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        if self.current_user['role'] == 'admin':
            self.current_frame = AdminMenu(self.root, self.theme_config, self.fonts)
        else:
            self.current_frame = UserMenu(self.root, self.current_user, self.theme_config, self.fonts)
