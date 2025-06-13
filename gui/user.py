from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QLabel, QLineEdit, 
                            QGroupBox, QMessageBox)
from services.tour_service import get_all_tours
from services.order_service import book_tour, purchase_tour

class UserPanel(QWidget):
    def __init__(self, user_data, logout_callback):
        super().__init__()
        self.user_data = user_data
        self.logout_callback = logout_callback
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        

        self.search_tab = QWidget()
        self.setup_search_tab()
        self.tabs.addTab(self.search_tab, "Поиск туров")
        

        self.bookings_tab = QWidget()
        self.tabs.addTab(self.bookings_tab, "Мои брони")

        self.purchases_tab = QWidget()
        self.tabs.addTab(self.purchases_tab, "Мои покупки")
        

        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.logout_callback)
        layout.addWidget(logout_btn)
    
    def setup_search_tab(self):
        layout = QVBoxLayout(self.search_tab)

        filter_group = QGroupBox("Фильтры")
        filter_layout = QHBoxLayout(filter_group)
        
        filter_layout.addWidget(QLabel("Страна:"))
        self.country_input = QLineEdit()
        filter_layout.addWidget(self.country_input)
        
        filter_layout.addWidget(QLabel("Город:"))
        self.city_input = QLineEdit()
        filter_layout.addWidget(self.city_input)
        
        filter_layout.addWidget(QLabel("Макс. цена:"))
        self.price_input = QLineEdit()
        filter_layout.addWidget(self.price_input)
        
        search_btn = QPushButton("Поиск")
        search_btn.clicked.connect(self.search_tours)
        filter_layout.addWidget(search_btn)
        
        layout.addWidget(filter_group)

        self.tours_table = QTableWidget()
        self.tours_table.setColumnCount(8)
        self.tours_table.setHorizontalHeaderLabels(
            ["ID", "Название", "Страна", "Город", "Цена", "Дата начала", "Дата окончания", "Места"]
        )
        self.tours_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tours_table)
        
        btn_layout = QHBoxLayout()
        
        view_btn = QPushButton("Просмотреть")
        view_btn.clicked.connect(self.view_tour)
        btn_layout.addWidget(view_btn)
        
        book_btn = QPushButton("Забронировать")
        book_btn.clicked.connect(self.book_tour)
        btn_layout.addWidget(book_btn)
        
        buy_btn = QPushButton("Купить")
        buy_btn.clicked.connect(self.buy_tour)
        btn_layout.addWidget(buy_btn)
        
        layout.addLayout(btn_layout)

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
    
    def search_tours(self):
        
        pass
    
    def view_tour(self):
        selected = self.tours_table.currentRow()
        if selected == -1:
            return
            
        tour_id = self.tours_table.item(selected, 0).text()
        self.show_tour_details(tour_id)
    
    def show_tour_details(self, tour_id):
        
        QMessageBox.information(self, "Детали тура", f"Просмотр тура с ID {tour_id}")
    
    def book_tour(self):
        selected = self.tours_table.currentRow()
        if selected == -1:
            return
            
        tour_id = self.tours_table.item(selected, 0).text()
        book_tour(self.user_data['id'], tour_id)
        QMessageBox.information(self, "Успех", "Тур забронирован")
    
    def buy_tour(self):
        selected = self.tours_table.currentRow()
        if selected == -1:
            return
            
        tour_id = self.tours_table.item(selected, 0).text()
        purchase_tour(self.user_data['id'], tour_id)
        QMessageBox.information(self, "Успех", "Тур куплен")