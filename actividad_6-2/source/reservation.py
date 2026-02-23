"""
Módulo para la gestión de Reservaciones.
"""

from source.file_manager import FileManager
from source.hotel import Hotel
from source.customer import Customer


class Reservation:
    """Administra las reservaciones conectando Clientes y Hoteles."""
    FILE_PATH = "reservations.json"

    @classmethod
    def create_reservation(cls, res_id, customer_id, hotel_id):
        """Crea una reservación si hay habitaciones y el cliente existe."""
        customers = FileManager.load_data(Customer.FILE_PATH)
        if str(customer_id) not in customers:
            print("Error: Cliente no registrado.")
            return False

        if Hotel.reserve_room(hotel_id):
            data = FileManager.load_data(cls.FILE_PATH)
            data[str(res_id)] = {
                "customer_id": customer_id,
                "hotel_id": hotel_id
            }
            FileManager.save_data(cls.FILE_PATH, data)
            return True
        return False

    @classmethod
    def cancel_reservation(cls, res_id):
        """Cancela una reservación y libera la habitación del hotel."""
        data = FileManager.load_data(cls.FILE_PATH)
        res_id_str = str(res_id)
        if res_id_str in data:
            hotel_id = data[res_id_str]["hotel_id"]
            Hotel.cancel_reservation(hotel_id)
            del data[res_id_str]
            FileManager.save_data(cls.FILE_PATH, data)
            return True
        print("Error: Reservación no encontrada.")
        return False
