# gui/app.py
import tkinter as tk
from tkinter import ttk
from .auth import AuthFrame, RegisterFrame
from .admin import AdminPanel
from .user import UserPanel
from .shared import Theme

class TourAgencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Agency")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        self.theme = Theme()
        self.current_user = None
        self.current_frame = None
        
        self.setup_style()
        self.show_auth_frame()
    
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настройка стилей на основе темы
        style.configure('.', background=self.theme.current['bg'])
        style.configure('TFrame', background=self.theme.current['bg'])
        style.configure('TLabel', background=self.theme.current['bg'], foreground=self.theme.current['text'])
        style.configure('TButton', padding=8)
        
        style.configure('Primary.TButton', 
                      background=self.theme.current['primary'], 
                      foreground='white')
        
        style.configure('Secondary.TButton', 
                      background=self.theme.current['secondary'], 
                      foreground='white')
        
        style.configure('Title.TLabel', 
                      font=('Segoe UI', 24, 'bold'), 
                      foreground=self.theme.current['primary'])
    
    def show_auth_frame(self):
        self.clear_frame()
        self.current_frame = AuthFrame(
            self, 
            on_login_success=self.on_login_success,
            switch_to_register=lambda: self.show_register_frame()
        )
        self.current_frame.pack(expand=True, fill=tk.BOTH)
    
    def show_register_frame(self):
        self.clear_frame()
        self.current_frame = RegisterFrame(
            self,
            on_back=self.show_auth_frame,
            on_register_success=self.show_auth_frame
        )
        self.current_frame.pack(expand=True, fill=tk.BOTH)
    
    def on_login_success(self, user_data):
        self.current_user = user_data
        self.show_main_panel()
    
    def show_main_panel(self):
        self.clear_frame()
        
        if self.current_user['role'] == 'admin':
            self.current_frame = AdminPanel(self, self.current_user)
        else:
            self.current_frame = UserPanel(self, self.current_user)
            
        self.current_frame.pack(expand=True, fill=tk.BOTH)
        
        # Добавляем кнопку выхода
        logout_btn = ttk.Button(
            self.current_frame, 
            text="Выйти", 
            command=self.logout,
            style='Danger.TButton'
        )
        logout_btn.pack(side=tk.BOTTOM, pady=10)
    
    def logout(self):
        self.current_user = None
        self.show_auth_frame()
    
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

if __name__ == "__main__":
    app = TourAgencyApp()
    app.mainloop()