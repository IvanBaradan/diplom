# gui/user.py
import tkinter as tk
from tkinter import ttk, messagebox
from services.tour_service import get_all_tours
from services.order_service import book_tour, purchase_tour
from services.review_service import add_review, get_reviews_for_tour

class UserPanel(ttk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.user_data = user_data
        self.create_widgets()
        
    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # Вкладка поиска туров
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="Поиск туров")
        self.setup_search_tab()
        
        # Вкладка моих бронирований
        self.bookings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bookings_frame, text="Мои брони")
        
        # Вкладка моих покупок
        self.purchases_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.purchases_frame, text="Мои покупки")
    
    def setup_search_tab(self):
        # Фильтры поиска
        filter_frame = ttk.LabelFrame(self.search_frame, text="Фильтры")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Страна:").grid(row=0, column=0, padx=5, pady=2)
        self.country_entry = ttk.Entry(filter_frame)
        self.country_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Город:").grid(row=0, column=2, padx=5, pady=2)
        self.city_entry = ttk.Entry(filter_frame)
        self.city_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Макс. цена:").grid(row=1, column=0, padx=5, pady=2)
        self.price_entry = ttk.Entry(filter_frame)
        self.price_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Button(filter_frame, text="Поиск", command=self.search_tours).grid(
            row=1, column=3, padx=5, pady=2)
        
        # Таблица с результатами
        columns = ("ID", "Название", "Страна", "Город", "Цена", "Дата начала", "Дата окончания", "Места")
        self.tours_tree = ttk.Treeview(self.search_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tours_tree.heading(col, text=col)
            self.tours_tree.column(col, width=100)
            
        self.tours_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Кнопки действий
        btn_frame = ttk.Frame(self.search_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Просмотреть", command=self.view_tour).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Забронировать", command=self.book_tour).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Купить", command=self.buy_tour).pack(side=tk.LEFT)
        
        # Загрузка всех туров при старте
        self.load_tours()
    
    def load_tours(self):
        for row in self.tours_tree.get_children():
            self.tours_tree.delete(row)
            
        for tour in get_all_tours():
            self.tours_tree.insert("", tk.END, values=(
                tour[0], tour[3], tour[1], tour[2], 
                f"{tour[4]} руб.", tour[5], tour[6], tour[8]
            ))
    
    def search_tours(self):
        # Реализация поиска по фильтрам
        pass
    
    def view_tour(self):
        selected = self.tours_tree.focus()
        if not selected:
            return
            
        tour_id = self.tours_tree.item(selected)['values'][0]
        self.show_tour_details(tour_id)
    
    def show_tour_details(self, tour_id):
        dialog = tk.Toplevel(self)
        dialog.title("Детали тура")
        
        # Здесь должна быть реализация просмотра деталей тура
        # с фотографией, описанием и отзывами
        
        ttk.Label(dialog, text="Отзывы:").pack()
        
        # Кнопки действий
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Забронировать", 
                  command=lambda: self.book_tour(tour_id)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Купить", 
                  command=lambda: self.buy_tour(tour_id)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Закрыть", 
                  command=dialog.destroy).pack(side=tk.RIGHT)
    
    def book_tour(self, tour_id=None):
        if not tour_id:
            selected = self.tours_tree.focus()
            if not selected:
                return
            tour_id = self.tours_tree.item(selected)['values'][0]
            
        book_tour(self.user_data['id'], tour_id)
        messagebox.showinfo("Успех", "Тур забронирован")
    
    def buy_tour(self, tour_id=None):
        if not tour_id:
            selected = self.tours_tree.focus()
            if not selected:
                return
            tour_id = self.tours_tree.item(selected)['values'][0]
            
        purchase_tour(self.user_data['id'], tour_id)
        messagebox.showinfo("Успех", "Тур куплен")