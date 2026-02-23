"""Pruebas unitarias para el módulo Reservation comprobando la integración."""

import unittest
import os
from source.hotel import Hotel
from source.customer import Customer
from source.reservation import Reservation


class TestReservation(unittest.TestCase):
    """Casos de prueba para la clase Reservation."""

    def setUp(self):
        """Limpia los archivos y crea datos base de prueba."""
        files = [
            Hotel.FILE_PATH,
            Customer.FILE_PATH,
            Reservation.FILE_PATH
        ]
        for file_name in files:
            if os.path.exists(file_name):
                os.remove(file_name)

        Hotel.create_hotel(1, "Hotel San Francisco", "San Francisco", 1)
        Customer.create_customer(101, "Emanuel", "emanuel@example.mx")

    def tearDown(self):
        """Limpia los archivos tras la prueba."""
        files = [
            Hotel.FILE_PATH,
            Customer.FILE_PATH,
            Reservation.FILE_PATH
        ]
        for file_name in files:
            if os.path.exists(file_name):
                os.remove(file_name)

    def test_create_and_cancel_reservation(self):
        """Prueba el ciclo de vida completo de una reservación."""
        result = Reservation.create_reservation("RES-001", 101, 1)
        self.assertTrue(result)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["rooms_available"], 0)

        cancel_result = Reservation.cancel_reservation("RES-001")
        self.assertTrue(cancel_result)
        hotel = Hotel.display_hotel(1)
        self.assertEqual(hotel["rooms_available"], 1)

    def test_negative_reserve_without_availability(self):
        """Caso Negativo: Reservar cuando se agotaron los cuartos."""
        Reservation.create_reservation("RES-001", 101, 1)
        result = Reservation.create_reservation("RES-002", 101, 1)
        self.assertFalse(result)

    def test_negative_unregistered_customer_reservation(self):
        """Caso Negativo: Reservar con cliente no registrado."""
        result = Reservation.create_reservation("RES-003", 999, 1)
        self.assertFalse(result)

    def test_negative_nonexistent_hotel_reservation(self):
        """Caso Negativo: Reservar en hotel inexistente."""
        result = Reservation.create_reservation("RES-004", 101, 999)
        self.assertFalse(result)

    def test_negative_cancel_nonexistent_reservation(self):
        """Caso Negativo: Cancelar reservación fantasma."""
        result = Reservation.cancel_reservation("RES-FALSA")
        self.assertFalse(result)
