from .vehicle import Vehicle

class Airplane(Vehicle):

    def __init__(self, capacity: float, max_altitude: float):
        super().__init__(capacity)
        if not isinstance(max_altitude, (int, float)) or max_altitude <= 0:
            raise ValueError("Максимальная высота должна быть положительным числом.")

        self.max_altitude = max_altitude

    def __str__(self):
        return (f"{super().__str__()}, "
                f"Максимальная высота: {self.max_altitude} м")
