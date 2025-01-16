from my_code.FormulaManager.FormulaProcessing import computeFormula
from my_code.DependencyManager import DependencyManager
from my_code.Cell import Cell
import re

class Spreadsheet:
    def __init__(self):
        self.cells = {}
        self.dependency_manager = DependencyManager()


    def edit_cell(self, coordinate, content):
        if not self._validate_coordinates(coordinate):
            raise ValueError(f"Invalid coordinate : {coordinate}")
        if not self._validate_content(content):
           raise ValueError("Invalid content type. Supported types are: str, int, float.")
        
        if isinstance(content, str) and content.startswith("="):
            from contentHandler.models.FormulaContent import FormulaContent

            #dependencies = self.dependency_manager.extract_dependencies(content)
            #self.dependency_manager.add_dependency(coordinate, dependencies)
            
            formula_content = FormulaContent(content[1:], self.dependency_manager)
            dependencies = formula_content.extractDependencies()

            if not self.dependency_manager.checkCircularDependency(coordinate, dependencies):
                raise ValueError(f"Circular dependency detected for cell {coordinate}.")
            

            self.dependency_manager.addDependency(coordinate, dependencies)
            cell_values = {coord: cell.getValue() for coord, cell in self.cells.items()}
            value = formula_content.calculateFormula(cell_values)
            self.set_cell_content(coordinate, formula_content)
            self.cells[coordinate].setValue(value)
        else:
            print(f"Editing cell {coordinate} with new content: {content}")
            self.set_cell_content(coordinate, content)
            self.cells[coordinate].setValue(content)
        
    def set_cell_content(self, coordinate, content):
        if coordinate not in self.cells:
            match = re.match(r"([A-Z]+)(\d+$)", coordinate)
            if not match:
                raise ValueError(f"Invalid coordinate : {coordinate}")
            col, row = match.groups()
            self.cells[coordinate] = Cell(col, row)
        #ERROR AQUI
        self.cells[coordinate].setContent(content)

    #def _split_coordinate(self, coordinate):
    #    import re
    #    match = re.match(r"^([A-Z]+)(\d+)$", coordinate)
    #    if not match:
    #        raise ValueError(f"Invalid coordinate format: {coordinate}")
    #    col, row = match.groups()
    #    return col, int(row)

    def get_cell_content(self, coordinate):
        if coordinate in self.cells:
            return self.cells[coordinate].getContent()
        else:
            return None
        #ValueError(f"Cell at {coordinate} does not exist.") we need this?

    def get_cell_value(self, coordinate):
        if coordinate in self.cells:
            #ERROR AQUI
            return self.cells[coordinate].getValue()
        else:
            raise ValueError(f"Cell at {coordinate} does not exist.")

    def _validate_coordinates(self, coordinate):
        # Validate coordinates like "A1", "B2", etc.
        return bool(re.match(r"^[A-Z]+\d+$", coordinate))
    
    def _validate_content(self, content):
        # Validate content type
        return isinstance(content, (str, int, float))

    def display_spreadsheet(self):
        # A simple way to display the spreadsheet
        rows = {}
        for coord, cell in self.cells.items():
            row, col = self._split_coordinate(coord)
            if row not in rows:
                rows[row] = {}
            rows[row][col] = cell.get_value() if cell.get_value() else ""
        
        # Print the table-like structure
        #all_rows = sorted(rows.keys(), key=lambda x: int(x))
        all_cols = sorted({col for row in rows.values() for col in row.keys()})
        print("\t" + "\t".join(all_cols))
        for row in sorted(rows.keys()):
        #for row in all_rows:
            print(row + "\t" + "\t".join(rows[row].get(col, "") for col in all_cols))

    def _split_coordinate(self, coordinate):
        # Split coordinates into row and column (e.g., "A1" -> "A", "1")
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
        return result        #FALTA UN RANGO??

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