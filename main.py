from transport.client import Client
from transport.vehicle import Vehicle
from transport.airplane import Airplane
from transport.van import Van
from transport.transport_company import TransportCompany

def get_float_input(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Значение должно быть положительным.")
                continue
            return value
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")

def get_bool_input(prompt: str) -> bool:
    while True:
        value = input(prompt + " (Да/Нет): ").strip().lower()
        if value in ('да', 'нет'):
            return value == 'да'
        print("Некорректный ввод. Пожалуйста, введите 'Да' или 'Нет'.")

def main_menu():
    company = TransportCompany("МойТранспорт")

    while True:
        print("\nМеню:")
        print("1. Добавить транспортное средство")
        print("2. Добавить клиента")
        print("3. Распределить грузы")
        print("4. Показать транспортные средства")
        print("5. Показать клиентов")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            print("\nВыберите тип транспортного средства:")
            print("1. Самолет")
            print("2. Фургон")
            vehicle_type = input("Введите номер типа: ")

            capacity = get_float_input("Введите грузоподъемность транспортного средства (в тоннах): ")

            if vehicle_type == "1":
                max_altitude = get_float_input("Введите максимальную высоту полета (в метрах): ")
                vehicle = Airplane(capacity, max_altitude)
            elif vehicle_type == "2":
                is_refrigerated = get_bool_input("Наличие холодильника")
                vehicle = Van(capacity, is_refrigerated)
            else:
                print("Некорректный выбор.")
                continue

            company.add_vehicle(vehicle)
            print(f"Транспортное средство добавлено: {vehicle}")

        elif choice == "2":
            name = input("Введите имя клиента: ")
            cargo_weight = get_float_input("Введите вес груза клиента (в тоннах): ")
            is_vip = get_bool_input("Клиент VIP?")
            client = Client(name, cargo_weight, is_vip)
            company.add_client(client)
            print(f"Клиент добавлен: {client}")

        elif choice == "3":
            company.optimize_cargo_distribution()
            print("Грузы распределены.")

        elif choice == "4":
            vehicles = company.list_vehicles()
            if not vehicles:
                print("Транспортные средства отсутствуют.")
            else:
                print("Список транспортных средств:")
                for vehicle in vehicles:
                    print(f"- {vehicle}")

        elif choice == "5":
            if not company.clients:
                print("Клиенты отсутствуют.")
            else:
                print("Список клиентов:")
                for client in company.clients:
                    print(f"- {client}")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
