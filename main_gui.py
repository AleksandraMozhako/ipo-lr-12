import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
from transport.client import Client
from transport.vehicle import Vehicle
from transport.airplane import Airplane
from transport.van import Van
from transport.transport_company import TransportCompany

class TransportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная компания")
        self.company = TransportCompany("МойТранспорт")

        # Создание меню
        self.create_menu()

        # Создание панели управления
        self.create_control_panel()

        # Создание таблиц
        self.create_tables()

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Кнопки удаления
        self.delete_client_button = ttk.Button(self.root, text="Удалить клиента", command=self.delete_client)
        self.delete_client_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_vehicle_button = ttk.Button(self.root, text="Удалить транспорт", command=self.delete_vehicle)
        self.delete_vehicle_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Привязка двойного щелчка для редактирования
        self.clients_tree.bind("<Double-1>", self.edit_client)
        self.vehicles_tree.bind("<Double-1>", self.edit_vehicle)

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Экспорт результата", command=self.export_data)
        file_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Файл", menu=file_menu)

        self.root.config(menu=menubar)

    def create_control_panel(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        ttk.Button(control_frame, text="Добавить клиента", command=lambda: self.show_add_client_window()).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Добавить транспорт", command=lambda: self.show_add_vehicle_window()).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Распределить грузы", command=self.optimize_cargo).pack(fill=tk.X, pady=5)

    def create_tables(self):
        tables_frame = ttk.Frame(self.root)
        tables_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Таблица клиентов
        clients_label = ttk.Label(tables_frame, text="Клиенты:")
        clients_label.pack(anchor=tk.W)

        self.clients_tree = ttk.Treeview(tables_frame, columns=("name", "cargo_weight", "is_vip"), show="headings")
        self.clients_tree.heading("name", text="Имя")
        self.clients_tree.heading("cargo_weight", text="Вес груза")
        self.clients_tree.heading("is_vip", text="VIP")
        self.clients_tree.pack(fill=tk.BOTH, expand=True)

        # Таблица транспортных средств
        vehicles_label = ttk.Label(tables_frame, text="Транспортные средства:")
        vehicles_label.pack(anchor=tk.W)

        self.vehicles_tree = ttk.Treeview(tables_frame, columns=("id", "type", "capacity", "current_load", "special_property"), show="headings")
        self.vehicles_tree.heading("id", text="ID")
        self.vehicles_tree.heading("type", text="Тип")
        self.vehicles_tree.heading("capacity", text="Грузоподъемность")
        self.vehicles_tree.heading("current_load", text="Текущая загрузка")
        self.vehicles_tree.heading("special_property", text="Специальное свойство")
        self.vehicles_tree.pack(fill=tk.BOTH, expand=True)

    def show_add_client_window(self, client=None):
        client_window = tk.Toplevel(self.root)
        client_window.title("Добавить клиента" if client is None else "Редактировать клиента")

        ttk.Label(client_window, text="Имя клиента:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(client_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(client_window, text="Вес груза:").grid(row=1, column=0, padx=5, pady=5)
        cargo_weight_entry = ttk.Entry(client_window)
        cargo_weight_entry.grid(row=1, column=1, padx=5, pady=5)

        is_vip_var = tk.BooleanVar()
        is_vip_check = ttk.Checkbutton(client_window, text="VIP статус", variable=is_vip_var)
        is_vip_check.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        if client:
            name_entry.insert(0, client.name)
            cargo_weight_entry.insert(0, str(client.cargo_weight))
            is_vip_var.set(client.is_vip)

        def save_client(existing_client=client):
            name = name_entry.get().strip()
            cargo_weight = cargo_weight_entry.get().strip()

            # Валидация имени
            if not name:
                messagebox.showerror("Ошибка", "Имя клиента обязательно для заполнения!")
                name_entry.delete(0, tk.END)
                return

            if len(name) < 2:
                messagebox.showerror("Ошибка", "Имя клиента должно содержать минимум 2 символа!")
                name_entry.delete(0, tk.END)
                return

            if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s]+$', name):
                messagebox.showerror("Ошибка", "Имя клиента должно содержать только буквы!")
                name_entry.delete(0, tk.END)
                return

            # Валидация веса груза
            if not cargo_weight:
                messagebox.showerror("Ошибка", "Вес груза обязателен для заполнения!")
                cargo_weight_entry.delete(0, tk.END)
                return

            try:
                cargo_weight = float(cargo_weight)
                if cargo_weight <= 0:
                    raise ValueError("Вес груза должен быть положительным числом!")
                if cargo_weight > 10000:
                    raise ValueError("Вес груза не должен превышать 10000 кг!")
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
                cargo_weight_entry.delete(0, tk.END)
                return

            if existing_client is not None:
                existing_client.name = name
                existing_client.cargo_weight = cargo_weight
                existing_client.is_vip = is_vip_var.get()
            else:
                new_client = Client(name, cargo_weight, is_vip_var.get())
                self.company.add_client(new_client)

            self.update_clients_table()
            client_window.destroy()
            self.status_var.set("Клиент сохранен.")

        ttk.Button(client_window, text="Сохранить", command=lambda: save_client(client)).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(client_window, text="Отмена", command=client_window.destroy).grid(row=3, column=1, padx=5, pady=5)

    def show_add_vehicle_window(self, vehicle=None):
        vehicle_window = tk.Toplevel(self.root)
        vehicle_window.title("Добавить транспорт" if vehicle is None else "Редактировать транспорт")

        # Тип транспорта
        ttk.Label(vehicle_window, text="Тип транспорта:").grid(row=0, column=0, padx=5, pady=5)
        vehicle_type_var = tk.StringVar()
        vehicle_type_combo = ttk.Combobox(vehicle_window, textvariable=vehicle_type_var, values=["Самолет", "Фургон"])
        vehicle_type_combo.grid(row=0, column=1, padx=5, pady=5)

        # Грузоподъемность
        ttk.Label(vehicle_window, text="Грузоподъемность:").grid(row=1, column=0, padx=5, pady=5)
        capacity_entry = ttk.Entry(vehicle_window)
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        # Динамическое поле для дополнительных параметров
        extra_frame = ttk.Frame(vehicle_window)
        extra_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        if vehicle:
            if isinstance(vehicle, Airplane):
                vehicle_type_var.set("Самолет")
                capacity_entry.insert(0, str(vehicle.capacity))
            elif isinstance(vehicle, Van):
                vehicle_type_var.set("Фургон")
                capacity_entry.insert(0, str(vehicle.capacity))

        # Функция для обновления дополнительного поля
        def update_extra_field(*args):
            for widget in extra_frame.winfo_children():
                widget.destroy()

            nonlocal extra_widget
            if vehicle_type_var.get() == "Самолет":
                ttk.Label(extra_frame, text="Макс. высота (м):").pack(side=tk.LEFT, padx=5, pady=5)
                max_altitude_entry = ttk.Entry(extra_frame)
                max_altitude_entry.pack(side=tk.LEFT, padx=5, pady=5)
                extra_widget = max_altitude_entry
                if vehicle and isinstance(vehicle, Airplane):
                    max_altitude_entry.insert(0, str(vehicle.max_altitude))
            else:
                is_refrigerated_var = tk.BooleanVar()
                is_refrigerated_check = ttk.Checkbutton(extra_frame, text="Холодильник", variable=is_refrigerated_var)
                is_refrigerated_check.pack(side=tk.LEFT, padx=5, pady=5)
                extra_widget = is_refrigerated_var
                if vehicle and isinstance(vehicle, Van):
                    is_refrigerated_var.set(vehicle.is_refrigerated)

        # Привязываем обновление поля к изменению типа транспорта
        vehicle_type_var.trace_add("write", update_extra_field)

        # Инициализируем поле
        extra_widget = None
        update_extra_field()

        def save_vehicle(existing_vehicle=vehicle):
            vehicle_type = vehicle_type_var.get()
            capacity = capacity_entry.get().strip()

            # Валидация грузоподъемности
            if not capacity:
                messagebox.showerror("Ошибка", "Грузоподъемность обязательна для заполнения!")
                capacity_entry.delete(0, tk.END)
                return

            try:
                capacity = float(capacity)
                if capacity <= 0:
                    raise ValueError("Грузоподъемность должна быть положительным числом!")
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
                capacity_entry.delete(0, tk.END)
                return

            if vehicle_type == "Самолет":
                max_altitude = extra_widget.get().strip()
                if not max_altitude:
                    messagebox.showerror("Ошибка", "Максимальная высота обязательна для заполнения!")
                    extra_widget.delete(0, tk.END)
                    return

                try:
                    max_altitude = float(max_altitude)
                    if max_altitude <= 0:
                        raise ValueError("Максимальная высота должна быть положительным числом!")
                except ValueError as e:
                    messagebox.showerror("Ошибка", str(e))
                    extra_widget.delete(0, tk.END)
                    return

                if existing_vehicle is not None and isinstance(existing_vehicle, Airplane):
                    existing_vehicle.capacity = capacity
                    existing_vehicle.max_altitude = max_altitude
                else:
                    new_vehicle = Airplane(capacity, max_altitude)
                    self.company.add_vehicle(new_vehicle)
            else:
                is_refrigerated = extra_widget.get()
                if existing_vehicle is not None and isinstance(existing_vehicle, Van):
                    existing_vehicle.capacity = capacity
                    existing_vehicle.is_refrigerated = is_refrigerated
                else:
                    new_vehicle = Van(capacity, is_refrigerated)
                    self.company.add_vehicle(new_vehicle)

            self.update_vehicles_table()
            vehicle_window.destroy()
            self.status_var.set("Транспортное средство сохранено.")

        ttk.Button(vehicle_window, text="Сохранить", command=lambda: save_vehicle(vehicle)).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(vehicle_window, text="Отмена", command=vehicle_window.destroy).grid(row=3, column=1, padx=5, pady=5)

    def edit_client(self, event):
        selected_item = self.clients_tree.selection()
        if not selected_item:
            return

        item_values = self.clients_tree.item(selected_item)["values"]
        name, cargo_weight, is_vip = item_values

        for client in self.company.clients:
            if client.name == name and client.cargo_weight == float(cargo_weight) and client.is_vip == (is_vip == "Да"):
                self.show_add_client_window(client)
                break

    def edit_vehicle(self, event):
        selected_item = self.vehicles_tree.selection()
        if not selected_item:
            return

        item_values = self.vehicles_tree.item(selected_item)["values"]
        vehicle_id = item_values[0]

        for vehicle in self.company.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                self.show_add_vehicle_window(vehicle)
                break

    def delete_client(self):
        selected_item = self.clients_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите клиента для удаления!")
            return

        item_values = self.clients_tree.item(selected_item)["values"]
        name, cargo_weight, is_vip = item_values

        for client in self.company.clients:
            if client.name == name and client.cargo_weight == float(cargo_weight) and client.is_vip == (is_vip == "Да"):
                self.company.clients.remove(client)
                self.update_clients_table()
                self.status_var.set("Клиент удален.")
                return

    def delete_vehicle(self):
        selected_item = self.vehicles_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите транспорт для удаления!")
            return

        item_values = self.vehicles_tree.item(selected_item)["values"]
        vehicle_id = item_values[0]

        for vehicle in self.company.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                self.company.vehicles.remove(vehicle)
                self.update_vehicles_table()
                self.status_var.set("Транспортное средство удалено.")
                return

    def update_clients_table(self):
        for row in self.clients_tree.get_children():
            self.clients_tree.delete(row)
        for client in self.company.clients:
            self.clients_tree.insert("", tk.END, values=(client.name, client.cargo_weight, "Да" if client.is_vip else "Нет"))

    def update_vehicles_table(self):
        for row in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(row)
        for vehicle in self.company.vehicles:
            if isinstance(vehicle, Airplane):
                special_property = f"Макс. высота полета: {vehicle.max_altitude} м"
            elif isinstance(vehicle, Van):
                special_property = "Холодильник" if vehicle.is_refrigerated else "Не холодильник"
            else:
                special_property = "Н/Д"

            self.vehicles_tree.insert("", tk.END, values=(
                vehicle.vehicle_id,
                vehicle.__class__.__name__,
                vehicle.capacity,
                vehicle.current_load,
                special_property
            ))

    def optimize_cargo(self):
        self.company.optimize_cargo_distribution()
        self.update_vehicles_table()
        self.status_var.set("Грузы распределены.")

    def export_data(self):
        if not self.company.clients and not self.company.vehicles:
            messagebox.showerror("Ошибка", "Нет данных для экспорта!")
            return

        data = {
            "clients": [
                {"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip}
                for c in self.company.clients
            ],
            "vehicles": [
                {
                    "id": v.vehicle_id,
                    "type": v.__class__.__name__,
                    "capacity": v.capacity,
                    "current_load": v.current_load,
                    "special_property": f"Максимальная высота полета: {v.max_altitude} м" if isinstance(v, Airplane) else ("Холодильник" if isinstance(v, Van) and v.is_refrigerated else "Не холодильник")
                }
                for v in self.company.vehicles
            ],
        }
        with open("transport_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.status_var.set("Данные экспортированы в transport_data.json.")

    def show_about(self):
        messagebox.showinfo("О программе", "Лабораторная работа №13\nВариант: 4\nРазработчик: Александра Можако")

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportApp(root)
    root.mainloop()
