from my_code.Spreadsheet import Spreadsheet
from my_code.SpreadsheetLoader import SpreadsheetLoader
from my_code.SpreadsheetSaver import SpreadsheetSaver
#from my_code.DependencyManager import DependencyManager
from contentHandler.models.Content import Content
from ui.UserInterface import UserInterface

class SpreadsheetController:
    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.userInterface = UserInterface()
        #self.dependencyManager = DependencyManager()
        self.newsheet: Spreadsheet = None

    def create_new_spreadsheet(self) -> Spreadsheet:
        self.spreadsheet = Spreadsheet()
        print("Nueva hoja de cálculo creada")

    #def set_cell_content(self, coordinate, content):
    #    try:
    #        if not coordinate or not content:
    #            raise ValueError("La coordenada o el contenido no pueden estar vacíos.")
    #        
    #        if isinstance(content, str) and content.startswith("="):
    #            dependencies = self.dependencyManager.extractDependencies(content)
    #            self.dependencyManager.addDependency(coordinate, dependencies)
    #            
    #    #Javi: se deberia de llamar aqui a edit_cell?
    #        self.spreadsheet.set_cell_content(coordinate, content)
    #        print(f"Contenido de la celda {coordinate} establecido a {content}")
    #    except Exception as e:
    #        print(f"Error al establecer el contenido de la celda: {e}")

    def get_cell_content(self, coordinate):
        try:
            content = self.spreadsheet.get_cell_content(coordinate)
            print(f"Contenido de la celda {coordinate}: {content}")
            return content
        except Exception as e:
            print(f"Error al obtener el contenido de la celda: {e}")
            return None
        
    def showMenu(self):
        self.userInterface.displayMenu()
        command = self.userInterface.getUserChoice()
        self.processCommand(command)

    def processCommand(self, command: str):
        """
        Processes a single command entered by the user or read from a file.
        """
        parts = command.split(maxsplit=2)
        cmd = parts[0]

        try:
            if cmd == "RF":
                if len(parts) < 2:
                    print("Error: Missing file path for RF command.")
                else:
                    self.readCommandsFromFile(parts[1])
            elif cmd == "C":
                self.create_new_spreadsheet()
            elif cmd == "E":
                if len(parts) < 3:
                    print("Error: Missing arguments for E command.")
                else:
                    self.set_cell_content(parts[1], parts[2])
                    self.printSpreadsheet()
            elif cmd == "L":
                if len(parts) < 2:
                    print("Error: Missing file path for L command.")
                else:
                    self.load_spreadsheet_from_file(parts[1])
            elif cmd == "S":
                if len(parts) < 2:
                    print("Error: Missing file path for S command.")
                else:
                    self.save_spreadsheet_to_file(parts[1])
            else:
                print(f"Error: Unknown command {cmd}.")
        except Exception as e:
            print(f"Error al procesar el comando {cmd}: {e}")
            import traceback
            traceback.print_exc()

    def set_cell_content(self, coord, str_content):
        try:
            self.spreadsheet.edit_cell(coord, str_content)
            print(f"Content of cell {coord} set to {str_content}")
        except Exception as e:
            print(f"Error setting cell content: {e}")

    def get_cell_content_as_float(self, coord):
        try:
            content = self.spreadsheet.get_cell_content(coord)
            return content.getNumericalValue() if content else 0.0
        except Exception as e:
            print(f"Error getting cell content as float: {e}")
            raise

    def get_cell_content_as_string(self, coord):
        try:
            content = self.spreadsheet.get_cell_content(coord)
            return content.getValue() if content else ""
        except Exception as e:
            print(f"Error getting cell content as string: {e}")
            raise

    def get_cell_formula_expression(self, coord):
        try:
            formula = self.get_cell_content_as_string(coord)
            return formula.replace("=", "") if formula else ""
        except Exception as e:
            print(f"Error getting cell formula expression: {e}")
            raise

    def save_spreadsheet_to_file(self, s_name_in_user_dir):
        try:
            SpreadsheetSaver.save_spreadsheet(s_name_in_user_dir, self.spreadsheet)
            print(f"Spreadsheet to be saved {s_name_in_user_dir}")
        except Exception as e:
            print(f"Error saving spreadsheet to file: {e}")
            raise

    def load_spreadsheet_from_file(self, s_name_in_user_dir):
        try:
            self.spreadsheet = SpreadsheetLoader.load_spreadsheet(s_name_in_user_dir)
            print(f"Spreadsheet loaded from {s_name_in_user_dir}")
        except Exception as e:
            print(f"Error loading spreadsheet from file: {e}")
            raise

    def readCommandsFromFile(self, file_path: str):
        """
        Reads and processes commands from a file.
        """
        try:
            with open(file_path, "r") as file:
                for line in file:
                    print(f"Processing command: {line.strip()}")
                    self.processCommand(line.strip())
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}.")

    #Print por la terminal toda la informacion de la celda
    def printSpreadsheet(self):
        """
        Prints the spreadsheet in a format similar to an Excel sheet.
        """
        # Obtener los límites
        min_row, max_row, min_col, max_col = self.spreadsheet.getBoundaries()

        # Generar los encabezados de columnas (sin conversiones)
        col_headers = []
        current_col = min_col
        while current_col <= max_col:
            col_headers.append(current_col)
            current_col = chr(ord(current_col) + 1)

        # Imprimir encabezado de columnas
        print("    ", end="")  # Espacio inicial para el encabezado de filas
        for header in col_headers:
            print(f"{header:^10}", end="")  # Encabezados centrados
        print()

        # Imprimir las filas y contenido
        for row in range(min_row, max_row + 1):
            print(f"{row:<4}", end="")  # Número de fila alineado a la izquierda
            for col in col_headers:
                cell_content = self.spreadsheet.get_cell_content(f"{col}{row}")
                cell_value = cell_content.getValue() if cell_content else ""
                print(f"{cell_value:^10}", end="")  # Contenido de la celda centrado
            print()  # Nueva línea al final de cada fila
