from my_code.Spreadsheet import Spreadsheet
from my_code.SpreadsheetLoader import SpreadsheetLoader
from my_code.SpreadsheetSaver import SpreadsheetSaver
from my_code.DependencyManager import DependencyManager
from ui.UserInterface import UserInterface

class SpreadsheetController:
    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.userInterface = UserInterface()
        self.dependencyManager = DependencyManager()

    def edit_cell_content(self, coordinate, content):
        try:
            # Javi:Previous validation for empty content or coordinate before setting the content
            if not coordinate or not content:
                raise ValueError("La coordenada o el contenido no pueden estar vacíos.")
            
            # Javi:Update the dpendency manager if the content is a formula
            if isinstance(content, str) and content.startswith("="):
                dependencies = self.dependencyManager.extractDependencies(content)
                self.dependencyManager.addDependency(coordinate, dependencies)

            self.spreadsheet.edit_cell(coordinate, content)
            print(f"Contenido de la celda {coordinate} establecido a {content}")
        except Exception as e:
            print(f"Error al establecer el contenido de la celda: {e}")

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
                self.spreadsheet = Spreadsheet()
                print("Nueva hoja de cálculo creada")
                self.spreadsheet.display_spreadsheet()
            elif cmd == "E":
                if len(parts) < 3:
                    print("Error: Missing arguments for E command.")
                else:
                    self.edit_cell_content(parts[1], parts[2])
                    #self.spreadsheet.display_spreadsheet()
                    self.printSpreadsheet()
            elif cmd == "L":
                if len(parts) < 2:
                    print("Error: Missing file path for L command.")
                else:
                    self.spreadsheet = SpreadsheetLoader.load_spreadsheet(parts[1])
            elif cmd == "S":
                if len(parts) < 2:
                    print("Error: Missing file path for S command.")
                else:
                    SpreadsheetSaver.save_spreadsheet(parts[1], self.spreadsheet)
            else:
                print(f"Error: Unknown command {cmd}.")
        except Exception as e:
            print(f"Error al procesar el comando {cmd}: {e}")

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
