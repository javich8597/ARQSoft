from .Cell import Cell
import re

class Spreadsheet:
    def __init__(self):
        self.cells = {}

    def edit_cell(self, coordinate, content):
        if not self._validate_coordinates(coordinate):
            raise ValueError("Invalid cell coordinates.")
        print(f"Editing cell {coordinate} with new content: {content}")
        self.set_cell_content(coordinate, content)
        
    def set_cell_content(self, coordinate, content):
        if coordinate not in self.cells:
            match = re.match(r"([A-Z]+)(\d+$)", coordinate)
            if not match:
                raise ValueError(f"Invalid coordinate format: {coordinate}")
            col = match.group(1)
            row = match.group(2)
            self.cells[coordinate] = Cell(col, row)
        self.cells[coordinate].setContent(content)

    def get_cell_content(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].getContent()
        else:
            return None
        #ValueError(f"Cell at {coordinate} does not exist.") we need this?


    def get_cell_value(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].get_value()
        else:
            raise ValueError(f"Cell at {coordinate} does not exist.")

    def _validate_coordinates(self, coordinate):
        # Validate coordinates like "A1", "B2", etc.
        return bool(re.match(r"^[A-Z]+\d+$", coordinate))

    def display_spreadsheet(self):
        # A simple way to display the spreadsheet
        rows = {}
        for coord, cell in self.cells.items():
            row, col = self._split_coordinate(coord)
            if row not in rows:
                rows[row] = {}
            rows[row][col] = cell.get_value() if cell.get_value() else ""
        
        # Print the table-like structure
        all_cols = sorted({col for row in rows.values() for col in row.keys()})
        print("\t" + "\t".join(all_cols))
        for row in sorted(rows.keys()):
            print(row + "\t" + "\t".join(rows[row].get(col, "") for col in all_cols))

    def _split_coordinate(self, coordinate):
        # Split coordinates into row and column (e.g., "A1" -> "A", "1")
        import re
        match = re.match(r"^([A-Z]+)(\d+)$", coordinate)
        if match:
            return match.groups()
        else:
            raise ValueError("Invalid coordinate format.")
    def getCellValues(self):
        # Devuelve un diccionario con los valores de las celdas
        return {cell.getCoordinate(): cell.getValue() for cell in self.cells}
        #FALTA UN RANGO??

    def getBoundaries(self):
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