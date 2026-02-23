"""
Módulo para la gestión de lectura y escritura de archivos JSON.
"""

import json
import os


class FileManager:
    """Clase base para manejar la lectura y escritura de archivos JSON."""

    @staticmethod
    def load_data(file_path):
        """Lee datos desde un archivo JSON, manejando errores de formato."""
        if not os.path.exists(file_path):
            return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            print(f"Error de formato en el archivo {file_path}: {error}")
            return {}

    @staticmethod
    def save_data(file_path, data):
        """Guarda un diccionario de datos en un archivo JSON."""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
