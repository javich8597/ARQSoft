from my_code.Spreadsheet import Spreadsheet
import pandas as pd
import os

class SpreadsheetSaver:
    @staticmethod
    def save_spreadsheet(path: str, spreadsheet: Spreadsheet):
        try:
            # Extract data from cells and convert to DataFrame
            cells = spreadsheet.cells
            data_dict = {
                coord: SpreadsheetSaver._convert_value(cell)
                for coord, cell in cells.items() if cell and cell.get_content()
            }

            max_row = max(int(coord[1:]) for coord in data_dict)
            max_col = max(ord(coord[0]) for coord in data_dict)
            columns = [chr(c) for c in range(ord('A'), max_col + 1)]

            df = pd.DataFrame("", index=range(1, max_row + 1), columns=columns)
            for coord, value in data_dict.items():
                df.at[int(coord[1:]), coord[0]] = value
            
            # Delete empty columns
            df = df.loc[:, (df != "").any()] 

            if not path.endswith(".s2v"):
                path += ".s2v"
            
            with open(path, 'w') as file:
                for _, row in df.iterrows():
                    line = list(row)
                    while line and line[-1] == "":
                        line.pop()

                    formatted_cell = [
                        str(cell).replace(';', ',') if isinstance(cell, str) and '=' in cell else str(cell)
                        for cell in line
                    ]

                    file.write(";".join(formatted_cell) + "\n")
                    
        except Exception as e:
            raise RuntimeError(f"An error occurred while saving the file: {e}")

    @staticmethod
    def _convert_value(cell):
        """Convierte el valor de la celda a tipo adecuado o mantiene fórmulas como texto"""
        content = cell.get_content()
        if content is None or content == "":
            return ""
        try:
            if hasattr(content, 'formula'):
                return content.formula

            if hasattr(content, 'get_value'):
                value = content.get_value()

                float_value = float(value)
                if float_value.is_integer():
                    return int(float_value)
                return float_value
            
            return str(content)
        except (ValueError, TypeError):
            return str(content)

    @staticmethod
    def is_valid_path(filepath):
        return os.path.isdir(os.path.dirname(filepath)) or os.path.isfile(filepath)

    @staticmethod
    def if_file_exists(filepath):
        return os.path.exists(filepath)
