from .vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, capacity: float, is_refrigerated: bool = False):
        
        super().__init__(capacity)
        if not isinstance(is_refrigerated, bool):
            raise ValueError("Флаг наличия холодильника должен быть булевым значением.")

        self.is_refrigerated = is_refrigerated

    def __str__(self):
        return (f"{super().__str__()}, "
                f"Холодильник: {'Да' if self.is_refrigerated else 'Нет'}")
