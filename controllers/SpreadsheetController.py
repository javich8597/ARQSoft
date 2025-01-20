from my_code.Spreadsheet import Spreadsheet
from my_code.SpreadsheetLoader import SpreadsheetLoader
from my_code.SpreadsheetSaver import SpreadsheetSaver
from ui.UserInterface import UserInterface

class SpreadsheetController:
    def __init__(self):
        self.spreadsheet = Spreadsheet()
        self.userInterface = UserInterface()

    def create_new_spreadsheet(self) -> Spreadsheet:
        self.spreadsheet = Spreadsheet()
        print("Created new spreadsheet.")

    def get_cell_content(self, coordinate):
        try:
            content = self.spreadsheet.get_cell_content(coordinate)
            return content
        except Exception as e:
            print(f"Error in get_cell_content: {e}")
            return None
        
    def show_menu(self):
        self.userInterface.display_menu()
        command = self.userInterface.get_user_choice()
        self.process_command(command)

    def process_command(self, command: str):
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
                    self.read_commands_from_file(parts[1])
                    self.print_spreadsheet()
                    
            elif cmd == "C":
                self.create_new_spreadsheet()
            elif cmd == "E":
                if len(parts) < 3:
                    print("Error: Missing arguments for E command.")
                else:
                    self.set_cell_content(parts[1], parts[2])
                    self.print_spreadsheet()
                   
            elif cmd == "L":
                if len(parts) < 2:
                    print("Error: Missing file path for L command.")
                else:
                    self.load_spreadsheet_from_file(parts[1])
                    self.print_spreadsheet()
                   
            elif cmd == "S":
                if len(parts) < 2:
                    print("Error: Missing file path for S command.")
                else:
                    self.save_spreadsheet_to_file(parts[1])
                    self.print_spreadsheet()

            else:
                print(f"Error: Unknown command {cmd}.")
        except Exception as e:
            print(f"Error processing command {cmd}: {e}")


    def set_cell_content(self, coord, str_content):
        try:
            self.spreadsheet.edit_cell(coord, str_content)
            print(f"Content of cell {coord} set to {str_content}")
        except Exception as e:
            print(f"Error setting cell content: {e}")

    def get_cell_content_as_float(self, coord):
        try:
            content = self.spreadsheet.get_cell_content(coord)
            return content.get_number_value() if content else 0.0
        except Exception as e:
            print(f"Error getting cell content as float: {e}")
            raise

    def get_cell_content_as_string(self, coord) -> str:
        try:
            content = self.spreadsheet.get_cell_content(coord)
            return content.get_value() if content else ""
        except Exception as e:
            print(f"Error getting cell content as string: {e}")
            raise

    def get_cell_formula_expression(self, coord):
        try:
            formula = self.spreadsheet.get_cell_content(coord)
            return formula.formula
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

    def read_commands_from_file(self, file_path: str):
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


    def print_spreadsheet(self):
        """
        Prints the spreadsheet in a format similar to an Excel sheet,
        dynamically adjusting column widths based on the longest content.
        """
        # Obtain the boundaries of the spreadsheet
        min_row, max_row, min_col, max_col = self.spreadsheet.get_boundaries()

        # Generate column headers
        col_headers = []
        current_col = min_col
        while current_col <= max_col:
            col_headers.append(current_col)
            current_col = chr(ord(current_col) + 1)

        # Calculate column widths
        column_widths = {}
        for col in col_headers:
            max_width = len(col)  # Start with the length of the header
            for row in range(min_row, max_row + 1):
                cell_address = f"{col}{row}"
                cell_content = self.spreadsheet.get_cell_content(cell_address)
                if cell_content:
                    try:
                        formula = cell_content.formula
                        value = str(cell_content.get_value())
                        content_length = len(f"{formula} ({value})")
                    except AttributeError:
                        value = str(cell_content.get_value())
                        content_length = len(value)
                    max_width = max(max_width, content_length)
            column_widths[col] = max_width + 2  # Add padding for readability

        # Print the column headers
        print("    ", end="")  # Space for row numbers
        for col in col_headers:
            print(f"{col:^{column_widths[col]}}", end="")
        print()

        # Print the content of each cell
        for row in range(min_row, max_row + 1):
            print(f"{row:<4}", end="")  # Number of the row
            for col in col_headers:
                cell_address = f"{col}{row}"
                cell_content = self.spreadsheet.get_cell_content(cell_address)
                if cell_content:
                    try:
                        # Attempt to get the formula if it exists
                        formula = cell_content.formula
                        value = str(cell_content.get_value())
                        content = f"{formula} ({value})"
                    except AttributeError:
                        # If no formula, just print the value
                        content = str(cell_content.get_value())
                else:
                    # Empty cell
                    content = ""
                # Print the content, centered in its column
                print(f"{content:^{column_widths[col]}}", end="")
            print()  # New line after each row


