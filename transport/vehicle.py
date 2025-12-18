import random
import string
from .client import Client

class Vehicle:

    def __init__(self, capacity: float):
        
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом.")

        self.vehicle_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.capacity = capacity
        self.current_load = 0.0
        self.clients_list = []

    def load_cargo(self, client: Client):
        if not isinstance(client, Client):
            raise ValueError("Аргумент должен быть объектом класса Client.")

        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Превышена грузоподъемность транспортного средства.")

        self.current_load += client.cargo_weight
        self.clients_list.append(client)

    def __str__(self):
        return (f"ID транспорта: {self.vehicle_id}, "
                f"Грузоподъемность: {self.capacity} т, "
                f"Текущая загрузка: {self.current_load} т")
