from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt
from gui.auth import AuthFrame
from gui.admin import AdminPanel
from gui.user import UserPanel
import sys

class TourAgencyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency")
        self.resize(1200, 800)
        self.setMinimumSize(1000, 700)
        
        self.current_user = None
        self.setup_ui()
    
    def setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.auth_frame = AuthFrame(
            on_login_success=self.on_login_success,
            switch_to_register=self.show_register_frame
        )
        self.stacked_widget.addWidget(self.auth_frame)
        
        self.show_auth_frame()
    
    def show_auth_frame(self):
        self.stacked_widget.setCurrentWidget(self.auth_frame)
    
    def show_register_frame(self):
        if not hasattr(self, 'register_frame'):
            from gui.auth import RegisterFrame
            self.register_frame = RegisterFrame(
                on_back=self.show_auth_frame,
                on_register_success=self.show_auth_frame
            )
            self.stacked_widget.addWidget(self.register_frame)
        self.stacked_widget.setCurrentWidget(self.register_frame)
    
    def on_login_success(self, user_data):
        self.current_user = user_data
        self.show_main_panel()
    
    def show_main_panel(self):
        if self.current_user['role'] == 'admin':
            if not hasattr(self, 'admin_panel'):
                self.admin_panel = AdminPanel(self.current_user, self.logout)
                self.stacked_widget.addWidget(self.admin_panel)
            self.stacked_widget.setCurrentWidget(self.admin_panel)
        else:
            if not hasattr(self, 'user_panel'):
                self.user_panel = UserPanel(self.current_user, self.logout)
                self.stacked_widget.addWidget(self.user_panel)
            self.stacked_widget.setCurrentWidget(self.user_panel)
    
    def logout(self):
        self.current_user = None
        self.show_auth_frame()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TourAgencyApp()
    window.show()
    sys.exit(app.exec_())