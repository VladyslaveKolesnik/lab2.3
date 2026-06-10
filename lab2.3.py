from enum import Enum
from dataclasses import dataclass

#  Перелічуваний тип (Enum)
class Room(Enum):
    KITCHEN = "Кухня"
    BEDROOM = "Спальня"
    GARAGE = "Гараж"

#  Базовий клас
class Device:
    def __init__(self, name: str, room: Room):
        if not name.strip():
            raise ValueError("Ім'я пристрою не може бути порожнім!") 
        self.name = name
        self.room = room
        self.is_on = False

    def turn_on(self) -> str:
        self.is_on = True
        return f"[{self.name}] Пристрій увімкнено."

    def get_info(self) -> str:
        status = "Увімкнено" if self.is_on else "Вимкнено"
        return f"Пристрій: {self.name} | Локація: {self.room.value} | Статус: {status}"

# Класи-нащадки (Наслідування та Поліморфізм)
class SmartLight(Device):
    def __init__(self, name: str, room: Room, brightness: int = 100):
        super().__init__(name, room)
        self.brightness = brightness
        
    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        if not (0 <= value <= 100):
            raise ValueError("Яскравість повинна бути від 0 до 100!")
        self._brightness = value

    def turn_on(self) -> str:
        self.is_on = True
        return f"[{self.name}] Світло увімкнено (Яскравість: {self.brightness}%)."

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} | Яскравість: {self.brightness}%"
class SmartThermostat(Device):
    def __init__(self, name: str, room: Room, temperature: float = 22.0):
        super().__init__(name, room)
        self.temperature = temperature
        
    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        if value < 10 or value > 40:
            raise ValueError("Неможлива температура для дому! Допустимо від 10 до 40 °C.")
        self._temperature = value
    def turn_on(self) -> str:
        self.is_on = True
        return f"[{self.name}] Клімат-контроль активовано (Цільова t: {self.temperature}°C)."

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info} | Температура: {self.temperature}°C"
#  Клас-менеджер (Композиція)
class HomeHub:
    def __init__(self):
        self._devices = []

    def add_device(self, device: Device):
        self._devices.append(device)
        print(f"Успішно підключено до хабу: {device.name}")

    def show_all(self):
        print("\n--- Всі пристрої у Smart Home ---")
        for d in self._devices:
            print(d.get_info())
        print("-------")

#  Специфіка: Контекст-менеджер "Нічний режим"
class NightMode:
    def __init__(self, hub: HomeHub):
        self.hub = hub
        self.saved_states = {}

    def __enter__(self):
        print("\nАктивація нічного режиму")
        for device in self.hub._devices:
            if isinstance(device, SmartLight):
                self.saved_states[device] = {'is_on': device.is_on, 'brightness': device.brightness}
                device.is_on = False
                device.brightness = 0
            elif isinstance(device, SmartThermostat):
                self.saved_states[device] = {'is_on': device.is_on, 'temperature': device.temperature}
                device.temperature = 18.0
        print("Світло вимкнено, температуру знижено до 18°C для комфортного сну.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("\nДеактивація нічного режиму (Ранок)")
        for device, state in self.saved_states.items():
            if isinstance(device, SmartLight):
                device.is_on = state['is_on']
                device.brightness = state['brightness']
            elif isinstance(device, SmartThermostat):
                device.is_on = state['is_on']
                device.temperature = state['temperature']
        print("Попередні налаштування всіх пристроїв відновлено.")
#  Блок взаємодії з користувачем через консоль
if __name__ == "__main__":
    print("--- Симулятор управління Розумним будинком ---")
    hub = HomeHub()
    room_map = {1: Room.KITCHEN, 2: Room.BEDROOM, 3: Room.GARAGE}

    try:
        # Додавання освітлення
        print("\nДодавання розумного освітлення:")
        l_name = input("Введіть назву : ")
        
        print("Оберіть кімнату: 1 - Кухня, 2 - Спальня, 3 - Гараж")
        l_room_choice = int(input("Ваш вибір (1/2/3): "))
        l_room = room_map.get(l_room_choice, Room.BEDROOM)
        
        l_brightness = int(input("Введіть яскравість (0-100): "))
        
        light = SmartLight(name=l_name, room=l_room, brightness=l_brightness)
        hub.add_device(light)

        # Додавання термостата
        print("\nДодавання клімат-контролю:")
        t_name = input("Введіть назву : ")
        
        print("Оберіть кімнату: 1 - Кухня, 2 - Спальня, 3 - Гараж")
        t_room_choice = int(input("Ваш вибір (1/2/3): "))
        t_room = room_map.get(t_room_choice, Room.BEDROOM)
        
        t_temp = float(input("Введіть цільову температуру (10-40): "))
        
        thermostat = SmartThermostat(name=t_name, room=t_room, temperature=t_temp)
        hub.add_device(thermostat)

        # Демонстрація поліморфізму
        print("\n--- Демонстрація поліморфізму (Увімкнення) ---")
        for device in hub._devices:
            print(device.turn_on())

        # Демонстрація контекст-менеджера
        with NightMode(hub):    
            hub.show_all()

        # Демонстрація архітектурного краш-тесту
        print("\n--- Спроба додати пристрій з неможливими налаштуваннями ---")
        bad_temp = float(input("Введіть неможливу температуру для термостата (наприклад, 100): "))
        broken_thermostat = SmartThermostat("Зламаний термостат", Room.GARAGE, temperature=bad_temp)

    except ValueError as e:
        print(f": Краш-тест: {e}")
    except Exception as e:
        print(f"Непередбачувана помилка: {e}")