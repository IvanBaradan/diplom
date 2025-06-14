# gui/user.py

import tkinter as tk
import random
import sys
import os

from tkinter import ttk, messagebox
from services import tour_service, order_service, review_service, pdf_generator
from gui import shared
from PIL import Image, ImageTk
import io
from services import review_service, tour_service


class UserMenu(ttk.Frame):
    def __init__(self, app, user, theme_config, fonts):
        super().__init__(app.root)
        self.app = app
        self.user = user
        self.theme_config = theme_config
        self.fonts = fonts
        self.pack(fill=tk.BOTH, expand=True)
        self.create_menu()

    def create_menu(self):
        ttk.Label(self, text=f"Добро пожаловать, {self.user['full_name']}!",
                  font=self.fonts['title'], foreground=self.theme_config['primary']).pack(pady=30)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        actions = [
            ("🔍 Поиск туров", self.show_all_tours),
            ("📌 Мои брони", self.view_my_bookings),
            ("🛒 Мои покупки", self.view_my_purchases),
            ("⭐ Оставить отзыв", self.leave_review),
            ("🚪 Выйти", self.app.logout),
        ]

        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(btn_frame, text=text, command=command, style='Primary.TButton')
            btn.grid(row=i, column=0, pady=5, ipadx=30, sticky='ew')

    def show_all_tours(self):
        window = tk.Toplevel(self)
        window.title("Поиск туров")
        window.geometry("1000x600")

        # Фильтры
        filter_frame = ttk.Frame(window)
        filter_frame.pack(pady=10, fill=tk.X)

        ttk.Label(filter_frame, text="Страна:").grid(row=0, column=0, padx=5)
        country_entry = ttk.Entry(filter_frame)
        country_entry.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Город:").grid(row=0, column=2, padx=5)
        city_entry = ttk.Entry(filter_frame)
        city_entry.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="Макс. цена:").grid(row=0, column=4, padx=5)
        price_entry = ttk.Entry(filter_frame)
        price_entry.grid(row=0, column=5, padx=5)

        def load_filtered_tours():
            country = country_entry.get().strip()
            city = city_entry.get().strip()
            try:
                max_price = int(price_entry.get()) if price_entry.get().strip() else None
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом")
                return

            tours = tour_service.filter_tours(
                country=country if country else None,
                city=city if city else None,
                max_price=max_price
            )
            update_tree(tours)

        ttk.Button(filter_frame, text="Поиск", command=load_filtered_tours).grid(row=0, column=6, padx=10)

        # Таблица туров
        tree = ttk.Treeview(window, columns=("ID", "Страна", "Город", "Название", "Цена", "Мест"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        def update_tree(tours):
            for i in tree.get_children():
                tree.delete(i)
            for tour in tours:
                tree.insert("", tk.END, values=(tour[0], tour[1], tour[2], tour[3], tour[4], tour[8]))

        def on_select(event):
            selected = tree.focus()
            if selected:
                values = tree.item(selected)['values']
                self.book_or_buy_popup(values[0], values[3])

        tree.bind("<Double-1>", on_select)

        # Загрузка всех туров по умолчанию
        update_tree(tour_service.get_all_tours())

        

    def book_or_buy_popup(self, tour_id, tour_name):
        tour = tour_service.get_tour_by_id(tour_id)
        if not tour:
            messagebox.showerror("Ошибка", "Информация о туре не найдена")
            return

        popup = tk.Toplevel(self)
        popup.title("Информация о туре")
        popup.geometry("600x600")

        # Изображение тура
        if tour[9]:
            try:
                image_data = tour[9]
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((300, 200))
                img = ImageTk.PhotoImage(image)
                img_label = ttk.Label(popup, image=img)
                img_label.image = img
                img_label.pack(pady=10)
            except Exception as e:
                ttk.Label(popup, text=f"Ошибка изображения: {e}").pack()
        else:
            ttk.Label(popup, text="Нет изображения для тура").pack(pady=5)

        # Название и детали
        ttk.Label(popup, text=tour[3], font=self.fonts['subtitle']).pack()
        ttk.Label(popup, text=f"{tour[1]}, {tour[2]}", font=self.fonts['normal']).pack()
        ttk.Label(popup, text=f"{tour[5]} - {tour[6]} | {tour[4]} руб.", font=self.fonts['normal']).pack(pady=5)

        # Описание
        ttk.Label(popup, text="Описание:", font=self.fonts['bold']).pack(anchor='w', padx=10)
        desc = tk.Text(popup, height=5, wrap='word')
        desc.insert(tk.END, tour[7])
        desc.configure(state='disabled')
        desc.pack(fill=tk.X, padx=10)

        # Средний рейтинг
        rating = review_service.get_average_rating(tour_id)
        ttk.Label(popup, text=f"⭐ Рейтинг: {rating if rating else 'Нет оценок'}").pack(pady=5)

        # Отзывы
        reviews = review_service.get_reviews_for_tour(tour_id)
        if reviews:
            ttk.Label(popup, text="Отзывы:", font=self.fonts['bold']).pack(anchor='w', padx=10)
            for rate, comment, user in reviews:
                ttk.Label(popup, text=f"{user}: {rate}/5 — {comment}", wraplength=500, justify='left').pack(anchor='w', padx=15)
        else:
            ttk.Label(popup, text="Нет отзывов", font=self.fonts['small']).pack()

        # Кнопки
        ttk.Button(popup, text="Забронировать", command=lambda: self.book(tour_id, popup),
                style='Secondary.TButton').pack(pady=5)
        ttk.Button(popup, text="Купить", command=lambda: self.purchase(tour_id, popup),
                style='Primary.TButton').pack(pady=5)
        
    def filter_tours_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Фильтрация туров")

        ttk.Label(popup, text="Страна:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        country_entry = ttk.Entry(popup)
        country_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(popup, text="Город:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        city_entry = ttk.Entry(popup)
        city_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(popup, text="Макс. цена:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        price_entry = ttk.Entry(popup)
        price_entry.grid(row=2, column=1, padx=5, pady=5)

        def apply_filter():
            country = country_entry.get().strip()
            city = city_entry.get().strip()
            try:
                max_price = int(price_entry.get().strip()) if price_entry.get().strip() else None
            except ValueError:
                messagebox.showerror("Ошибка", "Цена должна быть числом")
                return

            results = tour_service.filter_tours(
                country=country or None,
                city=city or None,
                max_price=max_price
            )

            if not results:
                messagebox.showinfo("Результаты", "Туры не найдены по заданным параметрам.")
                return

            result_win = tk.Toplevel(popup)
            result_win.title("Результаты фильтрации")

            tree = ttk.Treeview(result_win, columns=("ID", "Страна", "Город", "Название", "Цена", "Мест"), show='headings')
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            for col in tree["columns"]:
                tree.heading(col, text=col)

            for tour in results:
                tree.insert("", tk.END, values=(tour[0], tour[1], tour[2], tour[3], tour[4], tour[8]))

            def on_select(event):
                selected = tree.focus()
                if selected:
                    values = tree.item(selected)['values']
                    self.book_or_buy_popup(values[0], values[3])

            tree.bind("<Double-1>", on_select)

        ttk.Button(popup, text="Фильтровать", command=apply_filter, style='Primary.TButton').grid(row=3, column=0, columnspan=2, pady=10)


    def book(self, tour_id, popup):
        order_service.book_tour(self.user['id'], tour_id)
        messagebox.showinfo("Успех", "Тур забронирован.")
        popup.destroy()

    def purchase(self, tour_id, popup):
        order_service.purchase_tour(self.user['id'], tour_id)

        # Получаем данные для чека
        tour = tour_service.get_tour_by_id(tour_id)
        tour_name = tour[3]
        price = tour[4]
        username = self.user['username']
        order_id = random.randint(10000, 99999)  # В идеале — получить настоящий ID заказа

        path = pdf_generator.generate_pdf_receipt(order_id, tour_name, username, price)
        messagebox.showinfo("Успех", f"Тур куплен.\nЧек сохранён:\n{path}")
        popup.destroy()

    def view_my_bookings(self):
        self._show_orders_by_status(["booked"], "Мои брони")

    def view_my_purchases(self):
        self._show_orders_by_status(["purchased"], "Мои покупки")

    def view_my_refunds(self):
        self._show_orders_by_status(["refund_requested", "cancelled"], "Запросы на возврат")

    def _show_orders_by_status(self, statuses, title):
        orders = order_service.get_orders_by_user_and_status(self.user['id'], statuses)
        if not orders:
            messagebox.showinfo("Нет данных", f"{title} не найдены.")
            return

        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("900x600")
        
        # Стилизованный заголовок
        header_frame = ttk.Frame(win, style='Card.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header_frame, text=title, font=self.fonts['subtitle'], 
                foreground=self.theme_config['primary']).pack(pady=5)
        
        # Основное содержимое
        main_frame = ttk.Frame(win)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Таблица с заказами
        columns = ("ID", "Тур", "Статус", "Дата", "Цена")
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')
        
        # Настройка колонок
        tree.heading("ID", text="ID", anchor=tk.W)
        tree.heading("Тур", text="Тур", anchor=tk.W)
        tree.heading("Статус", text="Статус", anchor=tk.W)
        tree.heading("Дата", text="Дата", anchor=tk.W)
        tree.heading("Цена", text="Цена", anchor=tk.W)
        
        tree.column("ID", width=50, minwidth=50)
        tree.column("Тур", width=250, minwidth=150)
        tree.column("Статус", width=150, minwidth=100)
        tree.column("Дата", width=150, minwidth=100)
        tree.column("Цена", width=100, minwidth=80)
        
        # Добавляем данные
        for order in orders:
            tour = tour_service.get_tour_by_id(order[2])  # order[2] - tour_id
            price = tour[4] if tour else "N/A"
            tree.insert("", tk.END, values=(
                order[0],  # ID заказа
                order[1],  # Название тура
                order[4],  # Дата
                self._get_status_display(order[3]),  # Статус
                f"{price} ₽" if price != "N/A" else price
            ))
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки действий
        action_frame = ttk.Frame(win)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if "purchased" in statuses:
            ttk.Button(action_frame, text="Просмотреть чек", 
                    command=lambda: self._view_receipt(tree), 
                    style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        if "booked" in statuses:
            ttk.Button(action_frame, text="Отменить бронь", 
                    command=lambda: self._cancel_booking(tree),
                    style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Закрыть", 
                command=win.destroy,
                style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)
        
        # Обработка двойного клика
        tree.bind("<Double-1>", lambda e: self._show_order_details(tree))
        
    def _get_status_display(self, status):
        status_map = {
            'booked': '🟡 Забронирован',
            'purchased': '🟢 Оплачен',
            'refund_requested': '🟠 Возврат',
            'cancelled': '🔴 Отменен'
        }
        return status_map.get(status, status)
    
    def _view_receipt(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите заказ")
            return
        
        order_id = tree.item(selected)['values'][0]
        receipt_path = os.path.join("receipts", f"receipt_{order_id}.pdf")
        
        if os.path.exists(receipt_path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(receipt_path)
                else:  # macOS/Linux
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.run([opener, receipt_path], check=True)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть чек: {e}")
        else:
            messagebox.showwarning("Чек не найден", "Приносим извенения, чек не был найден.")
            
    def _cancel_booking(self, tree):
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите бронь")
            return
        
        order_id = tree.item(selected)['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите отменить бронь?"):
            order_service.request_refund(order_id)
            messagebox.showinfo("Успех", "Бронь отменена")
            tree.delete(selected)

    def _show_order_details(self, tree):
        selected = tree.focus()
        if not selected:
            return
        
        values = tree.item(selected)['values']
        order_id, tour_name, status, date, price = values
        
        details = f"""
        Информация о заказе:
        
        ID: {order_id}
        Тур: {tour_name}
        Статус: {status}
        Дата: {date}
        Цена: {price}
        """
        
        messagebox.showinfo("Детали заказа", details.strip())

    def leave_review(self):
        win = tk.Toplevel(self)
        win.title("Оставить отзыв")

        ttk.Label(win, text="ID тура:").pack()
        tour_id_entry = ttk.Entry(win)
        tour_id_entry.pack()

        ttk.Label(win, text="Оценка (1-5):").pack()
        rating_entry = ttk.Entry(win)
        rating_entry.pack()

        ttk.Label(win, text="Комментарий:").pack()
        comment_entry = ttk.Entry(win)
        comment_entry.pack()

        def submit():
            try:
                tour_id = int(tour_id_entry.get())
                rating = int(rating_entry.get())
                comment = comment_entry.get()
                review_service.add_review(self.user['id'], tour_id, rating, comment)
                messagebox.showinfo("Успех", "Отзыв отправлен.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Проверьте данные: {e}")

        ttk.Button(win, text="Отправить", command=submit, style='Primary.TButton').pack(pady=10)
