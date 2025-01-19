from my_code.Cell import Cell
from contentHandler.models.FormulaContent import FormulaContent
import re

class Spreadsheet:
    def __init__(self):
        self.cells = {}

    def edit_cell(self, coordinate, content):
        if not self._validate_coordinates(coordinate):
            raise ValueError("Invalid cell coordinates.")
        if not self._validate_content(content):
           raise ValueError("Invalid content type. Supported types are: str, int, float.")
        print(f"Editing cell {coordinate} with new content: {content}")
        
        try:
            self.set_cell_content(coordinate, content)
        except Exception as e:
            print(f"Exception in set_cell_content: {e}")
    
    def set_cell_content(self, coordinate, content):
        """
        Sets or updates the content of a cell in the spreadsheet.

        :param coordinate: The coordinate of the cell (e.g., 'A1').
        :param content_string: The content string to insert into the cell.
        """
        match = re.match(r"([A-Z]+)(\d+$)", coordinate)
        if not match:
            raise ValueError(f"Invalid coordinate format: {coordinate}")
        col, row = match.groups()
        
        if coordinate not in self.cells or len(self.cells)==0 :
            cell = Cell(col, row, content, self)
        else:
            cell = self.cells[coordinate]

        # Insert content into the cell (this also calculates the formula if applicable)
        cell.insert_content(content)
        self.cells[coordinate] = cell


    def get_cell_content(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].get_content()
        else:
            return None

    def _validate_coordinates(self, coordinate):
        # Validate coordinates like "A1", "B2", etc.
        return bool(re.match(r"^[A-Z]+\d+$", coordinate))
    
    def _validate_content(self, content):
        # Validate content type
        return isinstance(content, (str, int, float))

    def get_boundaries(self):
        """
        Gets the boundaries of the spreadsheet based on the initialized cells.
        :return: Tuple (min_row, max_row, min_col, max_col).
        """
        if not self.cells:
            return 1, 1, "A", "A"  # Default boundaries for an empty spreadsheet

        rows = []
        cols = []

        for coord in self.cells.keys():
            col, row = "", ""
            for char in coord:
                if char.isdigit():
                    row += char
                else:
                    col += char
            rows.append(int(row))
            cols.append(col)

        return min(rows), max(rows), min(cols), max(cols)

    def get_cells(self): 
        """
        Returns a dictionary with the content of all cells in the spreadsheet
        """
        cells_data = {}
        for coordinate, cell in self.cells.items():
            if cell.content:
                cells_data[coordinate] = cell.content
            else:
                cells_data[coordinate] = None
        return cells_data
