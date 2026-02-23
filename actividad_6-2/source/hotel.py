"""
Módulo para la gestión de Hoteles.
"""

from source.file_manager import FileManager


class Hotel:
    """Administra la información y el comportamiento de los hoteles."""
    FILE_PATH = "hotels.json"

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        """Crea un hotel y lo guarda en el archivo."""
        data = FileManager.load_data(cls.FILE_PATH)
        if str(hotel_id) in data:
            print(f"Error: El hotel con ID {hotel_id} ya existe.")
            return False
        if not isinstance(rooms, int) or rooms < 0:
            print("Error: El número de habitaciones debe ser válido.")
            return False

        data[str(hotel_id)] = {
            "name": name,
            "location": location,
            "rooms_available": rooms
        }
        FileManager.save_data(cls.FILE_PATH, data)
        return True

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel por su ID."""
        data = FileManager.load_data(cls.FILE_PATH)
        if str(hotel_id) in data:
            del data[str(hotel_id)]
            FileManager.save_data(cls.FILE_PATH, data)
            return True
        print(f"Error: Hotel {hotel_id} no encontrado.")
        return False

    @classmethod
    def display_hotel(cls, hotel_id):
        """Devuelve la información de un hotel."""
        data = FileManager.load_data(cls.FILE_PATH)
        return data.get(str(hotel_id))

    @classmethod
    def modify_hotel(cls, hotel_id, name=None, location=None, rooms=None):
        """Modifica los atributos de un hotel existente."""
        data = FileManager.load_data(cls.FILE_PATH)
        hotel_id_str = str(hotel_id)
        if hotel_id_str not in data:
            print("Error: No se puede modificar, el hotel no existe.")
            return False

        if name:
            data[hotel_id_str]["name"] = name
        if location:
            data[hotel_id_str]["location"] = location
        if rooms is not None and isinstance(rooms, int) and rooms >= 0:
            data[hotel_id_str]["rooms_available"] = rooms

        FileManager.save_data(cls.FILE_PATH, data)
        return True

    @classmethod
    def reserve_room(cls, hotel_id):
        """Disminuye la disponibilidad de habitaciones de un hotel en 1."""
        data = FileManager.load_data(cls.FILE_PATH)
        hotel_id_str = str(hotel_id)
        if hotel_id_str in data and data[hotel_id_str]["rooms_available"] > 0:
            data[hotel_id_str]["rooms_available"] -= 1
            FileManager.save_data(cls.FILE_PATH, data)
            return True
        print("Error: Hotel no encontrado o sin disponibilidad.")
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Aumenta la disponibilidad de habitaciones de un hotel en 1."""
        data = FileManager.load_data(cls.FILE_PATH)
        hotel_id_str = str(hotel_id)
        if hotel_id_str in data:
            data[hotel_id_str]["rooms_available"] += 1
            FileManager.save_data(cls.FILE_PATH, data)
            return True
        return False
