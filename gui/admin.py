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
            ("🧾 Все покупки", self.view_all_purchased_orders),
            ("↩ Возвраты", self.manage_refunds),
            ("👤 Пользователи", self.view_all_users),
            ("💬 Отзывы", self.view_all_reviews),
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
        tours = tour_service.get_all_tours()
        if not tours:
            messagebox.showinfo("Нет туров", "Список туров пуст.")
            return

        win = tk.Toplevel(self)
        win.title("Все туры")

        tree = ttk.Treeview(win, columns=("ID", "Страна", "Город", "Название", "Цена", "Дата от", "Дата до", "Описание", "Мест"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        for col in tree["columns"]:
            tree.heading(col, text=col)
        for row in tours:
            tree.insert("", tk.END, values=row)

        def delete_selected():
            selected = tree.focus()
            if selected:
                tour_id = tree.item(selected)['values'][0]
                if messagebox.askyesno("Удаление", "Удалить тур?"):
                    tour_service.delete_tour(tour_id)
                    tree.delete(selected)

        def edit_selected():
            selected = tree.focus()
            if selected:
                values = tree.item(selected)['values']
                self.edit_tour_window(values)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Удалить тур", command=delete_selected, style='Danger.TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Редактировать тур", command=edit_selected, style='Secondary.TButton').pack(side=tk.LEFT, padx=10)
        
    def view_all_purchased_orders(self):
        win = tk.Toplevel(self)
        win.title("Все покупки")

        # Форма фильтров
        filter_frame = ttk.Frame(win)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Пользователь:").grid(row=0, column=0, padx=5)
        user_entry = ttk.Entry(filter_frame, width=15)
        user_entry.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Тур:").grid(row=0, column=2, padx=5)
        tour_entry = ttk.Entry(filter_frame, width=15)
        tour_entry.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5)
        date_entry = ttk.Entry(filter_frame, width=12)
        date_entry.grid(row=0, column=5, padx=5)

        tree = ttk.Treeview(win, columns=("ID", "Пользователь", "Тур", "Дата"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        def load_data():
            user_f = user_entry.get().strip()
            tour_f = tour_entry.get().strip()
            date_f = date_entry.get().strip()

            orders = order_service.get_purchased_orders_filtered(
                user_filter=user_f or None,
                tour_filter=tour_f or None,
                date_filter=date_f or None
            )

            for i in tree.get_children():
                tree.delete(i)

            for order in orders:
                tree.insert("", tk.END, values=order)

        ttk.Button(filter_frame, text="Фильтровать", command=load_data).grid(row=0, column=6, padx=10)

        load_data()  # загрузка по умолчанию


    def edit_tour_window(self, tour_values):
        win = tk.Toplevel(self)
        win.title("Редактировать тур")
        keys = ["country", "city", "name", "price", "date_start", "date_end", "description", "seats"]
        fields = {}

        self.edited_image_data = tour_values[9] if len(tour_values) > 9 else None  # текущее изображение

        for i, key in enumerate(keys):
            ttk.Label(win, text=key.capitalize()).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            ent = ttk.Entry(win)
            ent.grid(row=i, column=1, padx=5, pady=3)
            ent.insert(0, str(tour_values[i + 1]))  # пропускаем ID
            fields[key] = ent

        # Кнопка загрузки изображения
        def load_image():
            from tkinter import filedialog
            path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.png *.jpeg *.gif")])
            if path:
                with open(path, 'rb') as f:
                    self.edited_image_data = f.read()
                ttk.Label(win, text="✅ Картинка загружена").grid(row=len(keys), column=1, sticky='w', padx=5)

        ttk.Button(win, text="Загрузить изображение", command=load_image).grid(row=len(keys), column=0, columnspan=2, pady=10)

        def save_changes():
            try:
                data = {k: f.get() for k, f in fields.items()}
                data["price"] = float(data["price"])
                data["seats"] = int(data["seats"])
                data["id"] = tour_values[0]
                data["image"] = self.edited_image_data  # добавляем картинку
                tour_service.update_tour(data)
                messagebox.showinfo("Готово", "Тур обновлён")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении: {e}")

        ttk.Button(win, text="Сохранить изменения", command=save_changes, style='Success.TButton').grid(row=len(keys)+1, column=0, columnspan=2, pady=10)


    def view_all_users(self):
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, full_name, phone, role FROM users")
        users = cur.fetchall()
        conn.close()

        win = tk.Toplevel(self)
        win.title("Пользователи")

        tree = ttk.Treeview(win, columns=("ID", "Логин", "ФИО", "Телефон", "Роль"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in tree["columns"]:
            tree.heading(col, text=col)
        for row in users:
            tree.insert("", tk.END, values=row)

        def delete_user():
            selected = tree.focus()
            if selected:
                user_id = tree.item(selected)['values'][0]
                if messagebox.askyesno("Удаление", "Удалить пользователя?"):
                    from services import auth_service
                    auth_service.delete_user(user_id)
                    tree.delete(selected)

        ttk.Button(win, text="Удалить пользователя", command=delete_user, style='Danger.TButton').pack(pady=10)


    def view_all_reviews(self):
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.id, u.username, t.name, o.rating, o.comment 
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN tours t ON o.tour_id = t.id
            WHERE o.rating IS NOT NULL
        """)
        reviews = cur.fetchall()
        conn.close()

        win = tk.Toplevel(self)
        win.title("Управление отзывами")
        win.geometry("900x500")

        # Стилизованный заголовок
        header_frame = ttk.Frame(win, style='Card.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text="Все отзывы", font=self.fonts['subtitle'], 
                foreground=self.theme_config['primary']).pack(pady=5)

        # Основное содержимое
        main_frame = ttk.Frame(win)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Таблица с отзывами
        columns = ("ID", "Пользователь", "Тур", "Оценка", "Комментарий")
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')

        # Настройка колонок
        tree.heading("ID", text="ID", anchor=tk.W)
        tree.heading("Пользователь", text="Пользователь", anchor=tk.W)
        tree.heading("Тур", text="Тур", anchor=tk.W)
        tree.heading("Оценка", text="Оценка", anchor=tk.W)
        tree.heading("Комментарий", text="Комментарий", anchor=tk.W)

        tree.column("ID", width=50, minwidth=50)
        tree.column("Пользователь", width=150, minwidth=100)
        tree.column("Тур", width=200, minwidth=150)
        tree.column("Оценка", width=80, minwidth=60)
        tree.column("Комментарий", width=400, minwidth=200)

        # Добавляем данные
        for review in reviews:
            rating = f"{review[3]}/5" if review[3] else "Без оценки"
            comment = review[4] if review[4] else "Без комментария"
            tree.insert("", tk.END, values=(
                review[0],  # ID отзыва
                review[1],  # Пользователь
                review[2],  # Тур
                rating,     # Оценка
                comment     # Комментарий
            ))

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        # Функция удаления отзыва
        def delete_review():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберите отзыв для удаления")
                return
            
            review_id = tree.item(selected)['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить выбранный отзыв?"):
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE orders SET rating=NULL, comment=NULL WHERE id=?", (review_id,))
                    conn.commit()
                    conn.close()
                    tree.delete(selected)
                    messagebox.showinfo("Успех", "Отзыв удален")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось удалить отзыв: {e}")

        # Кнопки действий
        action_frame = ttk.Frame(win)
        action_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(action_frame, text="Удалить отзыв", 
                command=delete_review,
                style='Danger.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(action_frame, text="Закрыть", 
                command=win.destroy,
                style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)

        # Обработка двойного клика
        def show_full_review(event):
            selected = tree.focus()
            if selected:
                values = tree.item(selected)['values']
                messagebox.showinfo("Полный отзыв", 
                                f"Пользователь: {values[1]}\nТур: {values[2]}\nОценка: {values[3]}\n\nКомментарий:\n{values[4]}")

        tree.bind("<Double-1>", show_full_review)

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
    
    def manage_refunds(self):
        orders = order_service.get_orders_with_status('refund_requested')
        if not orders:
            messagebox.showinfo("Нет запросов", "Нет активных запросов на возврат.")
            return

        win = tk.Toplevel(self)
        win.title("Запросы на возврат")

        tree = ttk.Treeview(win, columns=("ID", "Пользователь", "Тур"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        for row in orders:
            tree.insert("", tk.END, values=row)

        def approve():
            selected = tree.focus()
            if not selected:
                return
            order_id = tree.item(selected)['values'][0]
            order_service.approve_refund(order_id)
            messagebox.showinfo("Готово", "Возврат одобрен")
            tree.delete(selected)

        def reject():
            selected = tree.focus()
            if not selected:
                return
            order_id = tree.item(selected)['values'][0]
            order_service.reject_refund(order_id)
            messagebox.showinfo("Готово", "Возврат отклонён")
            tree.delete(selected)

        # 🔧 Оборачиваем кнопки в отдельный Frame
        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✅ Одобрить", command=approve).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="❌ Отклонить", command=reject).pack(side=tk.LEFT, padx=10)
