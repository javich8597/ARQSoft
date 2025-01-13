from code.Cell import Cell

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
            self.cells[coordinate] = Cell()
        self.cells[coordinate].setContent(content)

    def get_cell_content(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].get_content()
        else:
            raise ValueError(f"Cell at {coordinate} does not exist.")

    def get_cell_value(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].get_value()
        else:
            raise ValueError(f"Cell at {coordinate} does not exist.")

    def _validate_coordinates(self, coordinate):
        # Validate coordinates like "A1", "B2", etc.
        import re
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