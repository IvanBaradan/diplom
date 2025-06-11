# gui/admin.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from services.tour_service import add_tour, get_all_tours
from services.user_service import get_all_users
from PIL import Image, ImageTk
import io

class AdminPanel(ttk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.user_data = user_data
        self.create_widgets()
        
    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # Вкладка управления турами
        self.tours_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tours_frame, text="Туры")
        self.setup_tours_tab()
        
        # Вкладка управления пользователями
        self.users_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="Пользователи")
        self.setup_users_tab()
    
    def setup_tours_tab(self):
        # Таблица с турами
        columns = ("ID", "Название", "Страна", "Город", "Цена", "Дата начала", "Дата окончания", "Места")
        self.tours_tree = ttk.Treeview(self.tours_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tours_tree.heading(col, text=col)
            self.tours_tree.column(col, width=100)
            
        self.tours_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Кнопки управления
        btn_frame = ttk.Frame(self.tours_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Добавить тур", command=self.show_add_tour_dialog).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Удалить тур").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Обновить").pack(side=tk.LEFT)
        
        # Загрузка данных
        self.load_tours()
    
    def show_add_tour_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Добавить тур")
        
        fields = [
            ("Название:", "name"),
            ("Страна:", "country"),
            ("Город:", "city"),
            ("Цена:", "price"),
            ("Дата начала (ГГГГ-ММ-ДД):", "date_start"),
            ("Дата окончания (ГГГГ-ММ-ДД):", "date_end"),
            ("Количество мест:", "seats"),
            ("Описание:", "description")
        ]
        
        entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(dialog) if field != "description" else tk.Text(dialog, height=5, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
            entries[field] = entry
            
        # Загрузка изображения
        self.tour_image = None
        ttk.Button(dialog, text="Выбрать изображение", command=lambda: self.load_tour_image(dialog)).grid(
            row=len(fields), columnspan=2, pady=5)
            
        # Кнопки
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=len(fields)+1, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Добавить", command=lambda: self.add_tour(entries)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT)
        
    def load_tour_image(self, dialog):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                image = Image.open(file_path)
                image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)
                
                if hasattr(self, 'image_label'):
                    self.image_label.destroy()
                    
                self.image_label = ttk.Label(dialog, image=photo)
                self.image_label.image = photo
                self.image_label.grid(row=0, column=2, rowspan=4, padx=10)
                
                with open(file_path, 'rb') as f:
                    self.tour_image = f.read()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")
    
    def add_tour(self, entries):
        data = {
            'name': entries['name'].get(),
            'country': entries['country'].get(),
            'city': entries['city'].get(),
            'price': float(entries['price'].get()),
            'date_start': entries['date_start'].get(),
            'date_end': entries['date_end'].get(),
            'seats': int(entries['seats'].get()),
            'description': entries['description'].get("1.0", tk.END).strip(),
            'image': self.tour_image
        }
        
        add_tour(data)
        messagebox.showinfo("Успех", "Тур добавлен")
        self.load_tours()
        
    def load_tours(self):
        for row in self.tours_tree.get_children():
            self.tours_tree.delete(row)
            
        for tour in get_all_tours():
            self.tours_tree.insert("", tk.END, values=(
                tour.id, tour.name, tour.country, tour.city, 
                f"{tour.price} руб.", tour.date_start, tour.date_end, tour.seats
            ))
    
    def setup_users_tab(self):
        # Таблица с пользователями
        columns = ("ID", "Логин", "ФИО", "Телефон", "Роль")
        self.users_tree = ttk.Treeview(self.users_frame, columns=columns, show="headings")
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
            
        self.users_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Кнопки управления
        btn_frame = ttk.Frame(self.users_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Удалить пользователя").pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Обновить", command=self.load_users).pack(side=tk.LEFT, padx=5)
        
        # Загрузка данных
        self.load_users()
    
    def load_users(self):
        for row in self.users_tree.get_children():
            self.users_tree.delete(row)
            
        for user in get_all_users():
            self.users_tree.insert("", tk.END, values=(
                user.id, user.username, user.full_name, user.phone, user.role
            ))