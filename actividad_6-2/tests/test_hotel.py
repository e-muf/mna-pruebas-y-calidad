"""Pruebas unitarias para el módulo Hotel."""

import unittest
import os
from source.hotel import Hotel


class TestHotel(unittest.TestCase):
    """Casos de prueba para la clase Hotel."""

    def setUp(self):
        """Prepara el entorno antes de cada prueba."""
        if os.path.exists(Hotel.FILE_PATH):
            os.remove(Hotel.FILE_PATH)
        Hotel.create_hotel(1, "Gran Hotel CDMX", "Ciudad de México", 50)

    def tearDown(self):
        """Limpia los archivos después de cada prueba."""
        if os.path.exists(Hotel.FILE_PATH):
            os.remove(Hotel.FILE_PATH)

    def test_create_and_display_hotel(self):
        """Prueba la creación exitosa y lectura de un hotel."""
        hotel = Hotel.display_hotel(1)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel["name"], "Gran Hotel CDMX")
        self.assertEqual(hotel["location"], "Ciudad de México")

    def test_display_nonexistent_hotel(self):
        """Buscar un hotel que no existe debe devolver None."""
        self.assertIsNone(Hotel.display_hotel(999))

    def test_modify_hotel_success(self):
        """Prueba la modificación de datos de un hotel."""
        result = Hotel.modify_hotel(1, name="Gran Hotel Zócalo", rooms=45)
        self.assertTrue(result)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["name"], "Gran Hotel Zócalo")
        self.assertEqual(hotel["rooms_available"], 45)

    def test_negative_create_existing_hotel(self):
        """Caso Negativo: Crear un hotel con un ID ya existente."""
        result = Hotel.create_hotel(1, "Bay View", "Mountain View", 20)
        self.assertFalse(result)

    def test_negative_invalid_room_count_negative(self):
        """Caso Negativo: Habitaciones negativas."""
        result = Hotel.create_hotel(2, "The Plaza", "New York", -10)
        self.assertFalse(result)

    def test_negative_invalid_room_count_type(self):
        """Caso Negativo: Enviar string en vez de entero."""
        result = Hotel.create_hotel(3, "Hotel SF", "San Francisco", "diez")
        self.assertFalse(result)

    def test_negative_modify_nonexistent_hotel(self):
        """Caso Negativo: Modificar un hotel que no existe."""
        result = Hotel.modify_hotel(999, name="Fantasma")
        self.assertFalse(result)

    def test_negative_delete_nonexistent_hotel(self):
        """Caso Negativo: Borrar hotel inexistente."""
        result = Hotel.delete_hotel(999)
        self.assertFalse(result)

    def test_negative_reserve_nonexistent_hotel(self):
        """Caso Negativo: Restar habitaciones a un hotel que no existe."""
        result = Hotel.reserve_room(999)
        self.assertFalse(result)

    def test_negative_cancel_reservation_nonexistent_hotel(self):
        """Caso Negativo: Sumar habitaciones a un hotel que no existe."""
        result = Hotel.cancel_reservation(999)
        self.assertFalse(result)
