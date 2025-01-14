from code.Cell import Cell

class Spreadsheet:
    def __init__(self):
        self.cells = {}
        # Javi: Rango de celdas predefinido si o no?
        #def __init__(self, rows=10, cols=10):
        #self.cells = {}
        #for row in range(1, rows + 1):
        #    for col in range(1, cols + 1):
        #        coordinate = f"{chr(64 + col)}{row}"
        #        self.cells[coordinate] = Cell()

    def edit_cell(self, coordinate, content):
        if not self._validate_coordinates(coordinate):
            raise ValueError("Invalid cell coordinates.")
        if not self._validate_content(content):
            raise ValueError("Invalid content type. Supported types are: str, int, float.")
        print(f"Editing cell {coordinate} with new content: {content}")
        self.set_cell_content(coordinate, content)
        
    def set_cell_content(self, coordinate, content):
        if coordinate not in self.cells:
            col, row = self._split_coordinate(coordinate)
            self.cells[coordinate] = Cell(row=row, col=col)
        self.cells[coordinate].setContent(content)

    def _split_coordinate(self, coordinate):
        import re
        match = re.match(r"^([A-Z]+)(\d+)$", coordinate)
        if not match:
            raise ValueError(f"Invalid coordinate format: {coordinate}")
        col, row = match.groups()
        return col, int(row)

    def get_cell_content(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].get_content()
        else:
            raise ValueError(f"Cell at {coordinate} does not exist.")

    def get_cell_value(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].getValue()
        else:
            raise ValueError(f"Cell at {coordinate} does not exist.")

    def _validate_coordinates(self, coordinate):
        # Validate coordinates like "A1", "B2", etc.
        import re
        return bool(re.match(r"^[A-Z]+\d+$", coordinate))
    
    def _validate_content(self, content):
        # Validate content type
        return isinstance(content, (str, int, float))

    def display_spreadsheet(self):
        # A simple way to display the spreadsheet
        rows = {}
        for coord, Cell in self.cells.items():
            row, col = self._split_coordinate(coord)
            if row not in rows:
                rows[row] = {}
            rows[row][col] = Cell.getValue() if Cell.getValue() else ""
        
        # Print the table-like structure
        all_rows = sorted(rows.keys(), key=lambda x: int(x))
        all_cols = sorted({col for row in rows.values() for col in row.keys()})
        print("\t" + "\t".join(all_cols))
        #for row in sorted(rows.keys()):
        for row in all_rows:
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
        #return {cell.getCoordinate(): cell.getValue() for cell in self.cells}
        result = {}
        for coord, cell in self.cells.items():
            value = cell.getValue()
            result[coord] = value if value is not None else ""
        return result
        #FALTA UN RANGO??