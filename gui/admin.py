# gui/admin.py

import tkinter as tk
import re

from tkinter import ttk, messagebox, filedialog
from services import tour_service, order_service, review_service, validators
from gui import shared
from PIL import Image, ImageTk

class AdminMenu(ttk.Frame):
    def __init__(self, app, theme_config, fonts):
        super().__init__(app.root)
        self.app = app
        self.theme_config = theme_config
        self.fonts = fonts
        self.tour_image_data = None
        self.pack(fill=tk.BOTH, expand=True)
        self.create_menu()

    def create_menu(self):
        ttk.Label(self, text="Панель администратора",
                  font=self.fonts['title'], foreground=self.theme_config['primary']).pack(pady=30)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        actions = [
            ("📦 Добавить тур", self.add_tour_window),
            ("🧭 Все туры", self.view_all_tours),
            ("👤 Пользователи", self.view_all_users),
            ("💬 Отзывы", self.view_all_reviews),
            ("↩ Запросы на возврат", self.view_all_refunds),
            ("🚪 Выйти", self.app.logout),
        ]

        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(btn_frame, text=text, command=command, style='Primary.TButton')
            btn.grid(row=i, column=0, pady=6, ipadx=40, sticky='ew')

    def add_tour_window(self):
        win = tk.Toplevel(self)
        win.title("Добавить тур")

        fields = {}
        labels = {
            'country': 'Страна',
            'city': 'Город',
            'name': 'Название',
            'price': 'Цена',
            'date_start': 'Дата начала (YYYY-MM-DD)',
            'date_end': 'Дата окончания (YYYY-MM-DD)',
            'description': 'Описание',
            'seats': 'Кол-во мест'
        }
        
        # Маска даты
        self.date_start_var = tk.StringVar()
        self.date_end_var = tk.StringVar()

        fields['date_start'] = ttk.Entry(win, textvariable=self.date_start_var)
        fields['date_end'] = ttk.Entry(win, textvariable=self.date_end_var)

        fields['date_start'].grid(row=4, column=1, padx=5, pady=5)
        fields['date_end'].grid(row=5, column=1, padx=5, pady=5)

        self.date_start_var.trace_add('write', self.on_date_change)
        self.date_end_var.trace_add('write', self.on_date_change)
        

        for i, (key, label) in enumerate(labels.items()):
            ttk.Label(win, text=label + ":").grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(win)
            entry.grid(row=i, column=1, padx=5, pady=5)
            fields[key] = entry

        image_btn = ttk.Button(win, text="Загрузить изображение", command=lambda: self.load_image(win))
        image_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

        ttk.Button(win, text="Сохранить", command=lambda: self.save_tour(fields, win),
                   style='Success.TButton').grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)
        
    def on_date_change(self, *_):
        for var in [self.date_start_var, self.date_end_var]:
            text = re.sub(r'\D', '', var.get())
            if len(text) > 8:
                text = text[:8]
            if len(text) >= 8:
                formatted = f"{text[:4]}-{text[4:6]}-{text[6:]}"
            elif len(text) >= 6:
                formatted = f"{text[:4]}-{text[4:6]}"
            elif len(text) >= 4:
                formatted = f"{text[:4]}"
            else:
                formatted = text
            var.set(formatted)

    def load_image(self, parent):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            with open(file_path, 'rb') as f:
                self.tour_image_data = f.read()

            img = Image.open(file_path)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(parent, image=photo)
            label.image = photo
            label.grid(column=0, columnspan=2)

    def save_tour(self, fields, win):
        try:
            data = {key: f.get() for key, f in fields.items()}
            data['price'] = float(data['price'])
            data['seats'] = int(data['seats'])
            data['image'] = self.tour_image_data
            tour_service.add_tour(data)
            messagebox.showinfo("Успех", "Тур добавлен.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверные данные: {e}")

    def view_all_tours(self):
        self._view_table("Все туры", tour_service.get_all_tours(), ("ID", "Страна", "Город", "Название", "Цена", "Дата от", "Дата до", "Описание", "Мест"))

    def view_all_users(self):
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, full_name, phone, role FROM users")
        users = cur.fetchall()
        conn.close()
        self._view_table("Пользователи", users, ("ID", "Логин", "ФИО", "Телефон", "Роль"))

    def view_all_reviews(self):
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, tour_id, rating, comment FROM orders WHERE rating IS NOT NULL")
        reviews = cur.fetchall()
        conn.close()
        self._view_table("Отзывы", reviews, ("ID", "Пользователь", "Тур", "Оценка", "Комментарий"))

    def view_all_refunds(self):
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, tour_id, status FROM orders WHERE status = 'refund_requested'")
        refunds = cur.fetchall()

        win = tk.Toplevel(self)
        win.title("Запросы на возврат")

        tree = ttk.Treeview(win, columns=("ID", "Пользователь", "Тур", "Статус"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        for row in refunds:
            tree.insert("", tk.END, values=row)

        def approve():
            selected = tree.focus()
            if selected:
                order_id = tree.item(selected)['values'][0]
                order_service.approve_refund(order_id)
                messagebox.showinfo("Успешно", "Возврат подтвержден")
                win.destroy()

        ttk.Button(win, text="Одобрить возврат", command=approve, style='Success.TButton').pack(pady=10)

    def _view_table(self, title, rows, columns):
        win = tk.Toplevel(self)
        win.title(title)

        tree = ttk.Treeview(win, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)

        for row in rows:
            tree.insert("", tk.END, values=row)
