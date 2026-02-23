"""
Módulo para la gestión de Clientes.
"""

from source.file_manager import FileManager


class Customer:
    """Administra la información y el comportamiento de los clientes."""
    FILE_PATH = "customers.json"

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Crea un nuevo cliente."""
        data = FileManager.load_data(cls.FILE_PATH)
        if str(customer_id) in data:
            print(f"Error: El cliente con ID {customer_id} ya existe.")
            return False

        data[str(customer_id)] = {"name": name, "email": email}
        FileManager.save_data(cls.FILE_PATH, data)
        return True

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente de los registros."""
        data = FileManager.load_data(cls.FILE_PATH)
        if str(customer_id) in data:
            del data[str(customer_id)]
            FileManager.save_data(cls.FILE_PATH, data)
            return True
        print(f"Error: Cliente {customer_id} no encontrado.")
        return False

    @classmethod
    def display_customer(cls, customer_id):
        """Muestra la información del cliente."""
        data = FileManager.load_data(cls.FILE_PATH)
        return data.get(str(customer_id))

    @classmethod
    def modify_customer(cls, customer_id, name=None, email=None):
        """Modifica la información de un cliente existente."""
        data = FileManager.load_data(cls.FILE_PATH)
        customer_id_str = str(customer_id)
        if customer_id_str not in data:
            print("Error: No se puede modificar, cliente no existe.")
            return False

        if name:
            data[customer_id_str]["name"] = name
        if email:
            data[customer_id_str]["email"] = email

        FileManager.save_data(cls.FILE_PATH, data)
        return True
