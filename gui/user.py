# gui/user.py

import tkinter as tk
import random

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
            ("↩ Запрос на возврат", self.view_my_refunds),
            ("⭐ Оставить отзыв", self.leave_review),
            ("🚪 Выйти", self.app.logout),
        ]

        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(btn_frame, text=text, command=command, style='Primary.TButton')
            btn.grid(row=i, column=0, pady=5, ipadx=30, sticky='ew')

    def show_all_tours(self):
        window = tk.Toplevel(self)
        window.title("Доступные туры")

        tours = tour_service.get_all_tours()
        if not tours:
            messagebox.showinfo("Нет туров", "Туры не найдены.")
            return

        tree = ttk.Treeview(window, columns=("ID", "Страна", "Город", "Название", "Цена", "Мест"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        for tour in tours:
            tree.insert("", tk.END, values=(tour[0], tour[1], tour[2], tour[3], tour[4], tour[8]))

        def on_select(event):
            selected = tree.focus()
            if selected:
                values = tree.item(selected)['values']
                self.book_or_buy_popup(values[0], values[3])

        tree.bind("<Double-1>", on_select)

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

        tree = ttk.Treeview(win, columns=("ID", "Тур", "Статус", "Дата"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        for order in orders:
            tree.insert("", tk.END, values=(order[0], order[1], order[2], order[3]))

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
