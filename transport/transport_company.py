from typing import List
from .client import Client
from .vehicle import Vehicle

class TransportCompany:

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Название компании должно быть строкой.")

        self.name = name
        self.vehicles: List[Vehicle] = []
        self.clients: List[Client] = []

    def add_vehicle(self, vehicle: Vehicle):
        if not isinstance(vehicle, Vehicle):
            raise ValueError("Аргумент должен быть транспортным средством.")

        self.vehicles.append(vehicle)

    def list_vehicles(self) -> List[Vehicle]:
        return self.vehicles

    def add_client(self, client: Client):
        if not isinstance(client, Client):
            raise ValueError("Аргумент должен быть клиентом.")

        self.clients.append(client)

    def optimize_cargo_distribution(self):
        
        sorted_clients = sorted(self.clients, key=lambda client: not client.is_vip)

        for client in sorted_clients:
            for vehicle in self.vehicles:
                try:
                    vehicle.load_cargo(client)
                    break
                except ValueError:
                    continue
