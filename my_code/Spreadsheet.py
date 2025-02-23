from my_code.Cell import Cell
from my_code.DependencyManager import DependencyManager
import re

class Spreadsheet:
    def __init__(self):
        self.cells = {}
        self.dependency_manager = DependencyManager()
        self.processing = set() #test3
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
        try:
            #print(f"Llamando a set_cell_content desde {self.__class__.__name__}")
            self.set_cell_content(coordinate, content)
        except Exception as e:
            print(f"Excepcion al llamar a set_cell_content: {e}")
    
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

        # Insertar contenido en la celda (esto tambien calcula la formula si aplica)
        cell.insertContent(content)
        self.cells[coordinate] = cell
        # Si el contenido es una formula, actualizamos dependencias en el DependencyManager
        if '=' in content:
            referenced_cells = getReferencedCells(content)

            # Eliminar dependencias antiguas y registrar nuevas
            self.dependency_manager.removeDependencies(coordinate) #AQUI
            self.dependency_manager.addDependencies(coordinate, referenced_cells)

        # Notificar a las celdas dependientes
        dependents = self.dependency_manager.getDependents(coordinate)
        for dependent in dependents:
            self.cells[dependent].insertContent(self.cells[dependent].content.formula)

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

    def getCells(self): #test2
        """
        Devuelve un diccionario con referencias de celdas como claves y sus contenidos como valores.
        """
        cells_data = {}
        for coordinate, cell in self.cells.items():
            if cell.content:
                # Devuelve el contenido de la celda directamente
                cells_data[coordinate] = cell.content
            else:
                cells_data[coordinate] = None
        return cells_data

def getReferencedCells(content): #test2
        """
        Extracts cell references (e.g., 'A2', 'A3') from the formula.
        """
        pattern = r"[A-Z]+[0-9]+"
        return re.findall(pattern, content)