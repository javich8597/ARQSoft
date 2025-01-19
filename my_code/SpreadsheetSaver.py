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
                coord: SpreadsheetSaver._convert_value(cell)  # Llamar a la función de conversión
                for coord, cell in cells.items() if cell
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
    def _convert_value(cell):
        """Convierte el valor de la celda a tipo adecuado o mantiene fórmulas como texto"""
        content = cell.get_content()
        if content is None or content == "":
            return ""  # Si la celda está vacía o es None, devolvemos una cadena vacía
        try:
            # Si el contenido es un objeto con una fórmula, devolver la fórmula como texto
            if hasattr(content, 'get_formula'):
                return content.get_formula()

            # Si el contenido es un objeto NumericalContent, obtener su valor numérico
            if hasattr(content, 'getValue'):
                value = content.getValue()

                # Intentar convertir a float primero
                float_value = float(value)
                # Si es un número entero (sin parte decimal), convertir a entero
                if float_value.is_integer():
                    return int(float_value)
                return float_value  # Si no es un número entero, devolver como float
            
            # Si no es una fórmula ni un valor numérico, devolver como texto
            return str(content)
        except (ValueError, TypeError):
            return str(content)  # Devolver como texto en caso de error

    @staticmethod
    def is_valid_path(filepath):
        return os.path.isdir(os.path.dirname(filepath)) or os.path.isfile(filepath)

    @staticmethod
    def if_file_exists(filepath):
        return os.path.exists(filepath)
