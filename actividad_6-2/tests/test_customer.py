"""Pruebas unitarias para el módulo Customer."""

import unittest
import os
from source.customer import Customer


class TestCustomer(unittest.TestCase):
    """Casos de prueba para la clase Customer."""

    def setUp(self):
        """Prepara los datos base de clientes."""
        if os.path.exists(Customer.FILE_PATH):
            os.remove(Customer.FILE_PATH)
        Customer.create_customer(101, "Emanuel", "emanuel@example.mx")
        Customer.create_customer(102, "Daniel", "daniel@example.mx")

    def tearDown(self):
        """Limpia los datos tras la prueba."""
        if os.path.exists(Customer.FILE_PATH):
            os.remove(Customer.FILE_PATH)

    def test_display_customer(self):
        """Valida que la información se despliegue correctamente."""
        customer = Customer.display_customer(101)
        self.assertEqual(customer["name"], "Emanuel")

    def test_display_nonexistent_customer(self):
        """Buscar cliente inexistente debe retornar None."""
        self.assertIsNone(Customer.display_customer(999))

    def test_delete_customer(self):
        """Prueba borrar un cliente existente."""
        result = Customer.delete_customer(101)
        self.assertTrue(result)
        self.assertIsNone(Customer.display_customer(101))

    def test_modify_customer_partial(self):
        """Prueba actualizar solo el correo sin afectar el nombre."""
        result = Customer.modify_customer(102, email="dan_nuevo@example.mx")
        self.assertTrue(result)
        customer = Customer.display_customer(102)
        self.assertEqual(customer["name"], "Daniel")
        self.assertEqual(customer["email"], "dan_nuevo@example.mx")

    def test_negative_create_existing_customer(self):
        """Caso Negativo: Crear cliente con ID repetido."""
        result = Customer.create_customer(101, "Clon de Emanuel", "clon@ex.mx")
        self.assertFalse(result)

    def test_negative_modify_nonexistent_customer(self):
        """Caso Negativo: Modificar cliente inexistente."""
        result = Customer.modify_customer(999, name="Desconocido")
        self.assertFalse(result)

    def test_negative_delete_nonexistent_customer(self):
        """Caso Negativo: Borrar cliente inexistente."""
        result = Customer.delete_customer(999)
        self.assertFalse(result)
