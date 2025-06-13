from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit, 
                            QTextEdit, QFileDialog, QMessageBox, QDateEdit, QSpinBox)
from PyQt5.QtCore import Qt, QDate
from services.tour_service import add_tour, get_all_tours
from services.user_service import get_all_users

class AdminPanel(QWidget):
    def __init__(self, user_data, logout_callback):
        super().__init__()
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        

        self.tours_tab = QWidget()
        self.setup_tours_tab()
        self.tabs.addTab(self.tours_tab, "Туры")
        

        self.users_tab = QWidget()
        self.setup_users_tab()
        self.tabs.addTab(self.users_tab, "Пользователи")
        

        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.logout_callback)
        layout.addWidget(logout_btn)
    
    def setup_tours_tab(self):
        layout = QVBoxLayout(self.tours_tab)
        

        self.tours_table = QTableWidget()
        self.tours_table.setColumnCount(8)
        self.tours_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Страна", "Город", "Цена", "Дата начала", "Дата окончания", "Места"]
        )
        self.tours_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tours_table)
        

        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить тур")
        add_btn.clicked.connect(self.show_add_tour_dialog)
        btn_layout.addWidget(add_btn)
        
        del_btn = QPushButton("Удалить тур")
        btn_layout.addWidget(del_btn)
        
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.load_tours)
        btn_layout.addWidget(refresh_btn)
        
        layout.addLayout(btn_layout)
        
        # Загрузка данных
        self.load_tours()
    
    def show_add_tour_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить тур")
        dialog.setModal(True)
        layout = QVBoxLayout(dialog)
        
        fields = [
            ("Название:", QLineEdit()),
            ("Страна:", QLineEdit()),
            ("Город:", QLineEdit()),
            ("Цена:", QLineEdit()),
            ("Дата начала:", QDateEdit(QDate.currentDate())),
            ("Дата окончания:", QDateEdit(QDate.currentDate())),
            ("Количество мест:", QSpinBox()),
            ("Описание:", QTextEdit())
        ]
        
        self.tour_image = None
        
        for label_text, widget in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)
        
        image_btn = QPushButton("Выбрать изображение")
        image_btn.clicked.connect(lambda: self.load_tour_image(dialog))
        layout.addWidget(image_btn)
        
        btn_row = QHBoxLayout()
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(lambda: self.add_tour(dialog, fields))
        btn_row.addWidget(add_btn)
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(dialog.reject)
        btn_row.addWidget(cancel_btn)
        
        layout.addLayout(btn_row)
        dialog.exec_()
    
    def load_tour_image(self, dialog):
        file_path, _ = QFileDialog.getOpenFileName(
            dialog, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg)")
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self.tour_image = f.read()
                QMessageBox.information(dialog, "Успех", "Изображение загружено")
            except Exception as e:
                QMessageBox.critical(dialog, "Ошибка", f"Не удалось загрузить изображение: {e}")
    
    def add_tour(self, dialog, fields):
        data = {
            'name': fields[0][1].text(),
            'country': fields[1][1].text(),
            'city': fields[2][1].text(),
            'price': float(fields[3][1].text()),
            'date_start': fields[4][1].date().toString(Qt.ISODate),
            'date_end': fields[5][1].date().toString(Qt.ISODate),
            'seats': fields[6][1].value(),
            'description': fields[7][1].toPlainText(),
            'image': self.tour_image
        }
        
        add_tour(data)
        QMessageBox.information(dialog, "Успех", "Тур добавлен")
        dialog.accept()
        self.load_tours()
    
    def load_tours(self):
        self.tours_table.setRowCount(0)
        tours = get_all_tours()
        self.tours_table.setRowCount(len(tours))
        
        for row, tour in enumerate(tours):
            self.tours_table.setItem(row, 0, QTableWidgetItem(str(tour.id)))
            self.tours_table.setItem(row, 1, QTableWidgetItem(tour.name))
            self.tours_table.setItem(row, 2, QTableWidgetItem(tour.country))
            self.tours_table.setItem(row, 3, QTableWidgetItem(tour.city))
            self.tours_table.setItem(row, 4, QTableWidgetItem(f"{tour.price} руб."))
            self.tours_table.setItem(row, 5, QTableWidgetItem(tour.date_start))
            self.tours_table.setItem(row, 6, QTableWidgetItem(tour.date_end))
            self.tours_table.setItem(row, 7, QTableWidgetItem(str(tour.seats)))

    def setup_users_tab(self):
        layout = QVBoxLayout(self.users_tab)
        

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Логин", "ФИО", "Телефон", "Роль"]
        )
        self.users_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.users_table)
        

        btn_layout = QHBoxLayout()
        
        del_btn = QPushButton("Удалить пользователя")
        btn_layout.addWidget(del_btn)
        
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.load_users)
        btn_layout.addWidget(refresh_btn)
        
        layout.addLayout(btn_layout)
    
        self.load_users()
    
    def load_users(self):
        self.users_table.setRowCount(0)
        users = get_all_users()
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.users_table.setItem(row, 1, QTableWidgetItem(user.username))
            self.users_table.setItem(row, 2, QTableWidgetItem(user.full_name))
            self.users_table.setItem(row, 3, QTableWidgetItem(user.phone))
            self.users_table.setItem(row, 4, QTableWidgetItem(user.role))