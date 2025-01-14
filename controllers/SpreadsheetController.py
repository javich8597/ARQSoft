
from ARQSoft.my_code.Spreadsheet import Spreadsheet
from ARQSoft.my_code.SpreadsheetLoader import SpreadsheetLoader
from ARQSoft.my_code.SpreadsheetSaver import SpreadsheetSaver
from ARQSoft.ui.UserInterface import UserInterface

class SpreadsheetController:
    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.userInterface = UserInterface()

#    def load_spreadsheet(self, file_path):
#        try:
#            self.spreadsheet = SpreadsheetLoader.load_spreadsheet(file_path)
#            print(f"Hoja de cálculo cargada desde {file_path}")
#        except Exception as e:
#            print(f"Error al cargar la hoja de cálculo: {e}")

#    def save_spreadsheet(self, file_path):
#        try:
#            SpreadsheetSaver.save_spreadsheet(file_path, self.spreadsheet)
#            print(f"Hoja de cálculo guardada en {file_path}")
#        except Exception as e:
#            print(f"Error al guardar la hoja de cálculo: {e}")

    def set_cell_content(self, coordinate, content):
        try:
            self.spreadsheet.set_cell_content(coordinate, content)
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

        if cmd == "RF":
            if len(parts) < 2:
                print("Error: Missing file path for RF command.")
            else:
                self.readCommandsFromFile(parts[1])
        elif cmd == "C":
            self.spreadsheet = Spreadsheet()
            print("Nueva hoja de cálculo creada")
        elif cmd == "E":
            if len(parts) < 3:
                print("Error: Missing arguments for E command.")
            else:
                self.spreadsheet.edit_cell(parts[1], parts[2])
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
