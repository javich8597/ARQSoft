from my_code.Spreadsheet import Spreadsheet
import pandas as pd
import os

class SpreadsheetSaver:
    @staticmethod
    def save_spreadsheet(path: str, spreadsheet: Spreadsheet):
        try:
            # Extraer celdas y crear un DataFrame directamente
            cells = spreadsheet.cells
            data_dict = {
                coord: SpreadsheetSaver._convert_value(cell.get_content())  # Llamar a la función de conversión
                for coord, cell in cells.items() if cell and cell.get_content()
            }

            # Determinar dimensiones de la hoja
            max_row = max(int(coord[1:]) for coord in data_dict)
            max_col = max(ord(coord[0]) for coord in data_dict)
            columns = [chr(c) for c in range(ord('A'), max_col + 1)]

            # Crear DataFrame y rellenar con los datos
            df = pd.DataFrame("", index=range(1, max_row + 1), columns=columns)
            for coord, value in data_dict.items():
                df.at[int(coord[1:]), coord[0]] = value

            # Guardar en archivo con extensión .s2v
            if not path.endswith(".s2v"):
                path += ".s2v"
            df.to_csv(path, sep=';', index=False, header=False)  # Guardar con punto y coma
        except Exception as e:
            raise RuntimeError(f"An error occurred while saving the file: {e}")

    @staticmethod
    def _convert_value(value):
        """Convierte el valor de la celda a tipo adecuado (int o float)"""
        if value is None or value == "":
            return ""  # Si la celda está vacía o es None, devolvemos una cadena vacía
        try:
            # Si el valor es un objeto NumericalContent, obtenemos su valor real
            if hasattr(value, 'getValue'):
                value = value.getValue()

            # Intentamos convertir a float primero
            float_value = float(value)
            # Si es un número entero (sin parte decimal), lo convertimos a entero
            if float_value.is_integer():
                return int(float_value)
            return float_value  # Si no es un número entero, devolvemos como float
        except ValueError:
            # Si no podemos convertir a float, devolvemos el valor tal cual (puede ser string o cualquier otro tipo)
            return value

    @staticmethod
    def is_valid_path(filepath):
        return os.path.isdir(os.path.dirname(filepath)) or os.path.isfile(filepath)

    @staticmethod
    def if_file_exists(filepath):
        return os.path.exists(filepath)