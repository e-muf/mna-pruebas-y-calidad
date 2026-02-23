"""Pruebas unitarias exclusivas para FileManager."""

import unittest
import os
from source.file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """Casos de prueba para la gestión de archivos JSON."""

    TEST_FILE = "test_data.json"

    def tearDown(self):
        """Limpia los archivos de prueba."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_load_nonexistent_file(self):
        """Si el archivo no existe, debe devolver un diccionario vacío."""
        data = FileManager.load_data("archivo_fantasma.json")
        self.assertEqual(data, {})

    def test_save_and_load_valid_data(self):
        """Prueba guardar y recuperar datos correctamente."""
        test_data = {"1": {"name": "Tacos El Vilsito", "rating": 5}}
        FileManager.save_data(self.TEST_FILE, test_data)

        loaded_data = FileManager.load_data(self.TEST_FILE)
        self.assertEqual(loaded_data, test_data)

    def test_load_corrupted_file(self):
        """
        Si el JSON está corrupto, debe ser capturado y no detener el sistema.
        """
        with open(self.TEST_FILE, "w", encoding='utf-8') as file:
            file.write("esto_no_es_un_json_valido")

        data = FileManager.load_data(self.TEST_FILE)
        self.assertEqual(data, {})
