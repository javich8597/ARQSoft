from my_code.Cell import Cell
import re

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
        try:
            #print(f"Llamando a set_cell_content desde {self.__class__.__name__}")
            self.set_cell_content(coordinate, content)
        except Exception as e:
            print(f"Excepción al llamar a set_cell_content: {e}")
        
    def set_cell_content(self, coordinate, content):
        #print(f"Creando celda con coordenada {coordinate} y contenido {content}")
        #print(f"spreadsheet: {self}") 
        try:
            #print("Entrando a set_cell_content")  # Esto imprimirá si el método se está ejecutando
            #print(f"type(self): {type(self)}")
            #if coordinate not in self.cells: #test
                match = re.match(r"([A-Z]+)(\d+$)", coordinate)
                if not match:
                    raise ValueError(f"Invalid coordinate format: {coordinate}")
                col, row = match.groups()
                if len(self.cells)==0 or not coordinate in self.cells:
                    cell = Cell(col, row, content, self)
                else:
                    cell = self.cells[coordinate]
                
                cell.insertContent(content)
                self.cells[coordinate] = cell
        except Exception as e:
            print(f"Ocurrió una excepción: {e}")    
        #self.cells[coordinate] = Cell(col, row, content, self.cells)    
        #ERROR AQUI - funcion de python?
        #self.cells[coordinate].setContent(content) hay que usar una funcion en cell para gestionar funciones

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

    def getCells(self): #test
        # Si necesitas devolver celdas con valores, puedes llenar self.cells_data aquí
        # Por ejemplo:
        self.cells_data = self.cells # O cualquier otra lógica que necesites
        return self.cells_data  # Devuelves el diccionario de celdas