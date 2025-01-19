from contentHandler.models.Content import Content
from my_code.FormulaManager.FormulaProcessing import computeFormula
from contentHandler.models.NumericalContent import NumericalContent
import re

class FormulaContent(Content):
    def __init__(self, formula: str, spreadsheet) -> None:
        super().__init__('formula', formula)
        self.formula = formula
        self.spreadsheet = spreadsheet
        

    def calculateFormula(self):
        try:
            # Evita recursion infinita usando un conjunto de celdas en proceso
            #if self.coordinate in self.spreadsheet.processing: #test3
                #raise CircularDependencyException(f"Circular dependency detected at {self.coordinate}")

            # Marca la celda como en proceso
            #self.spreadsheet.processing.add(self.coordinate)

            cell_values = self.spreadsheet.getCells() #test
            formula = self.formula
            #PRIMERO BUSCAR TODAS LAS REFERENCIAS A CELDAS Y SUSTITUIRLAS POR SU VALOR
            formula = self.process_references_cells(formula)
            #BUSCAR FUNCIONES EN LA FORMULA Y APLICARLAS AQUI
            formula = self.process_functions_formula(formula)
            

            #OJO ESTO TIENE QUE SER DESPUES DE HACER TODAS LAS FUNCIONES, SI NO PERDEMOS LOS RANGOS DE CELDAS POR EJEMPLO
            #Arreglamos la expresion de la formula primero 
            """
            try:
                
                # Reemplaza las referencias de celdas con sus valores
                pattern = r"\b[A-Z]+[0-9]+\b"  # Coincide con referencias exactas de celdas
                
                def replace_reference(match):
                    ref = match.group(0)
                    if ref in cell_values:
                        # Obtener el objeto y su valor numerico
                        cell_obj = cell_values[ref]
                        if isinstance(cell_obj, NumericalContent):
                            return str(cell_obj.getNumericalValue())
                        else:
                            raise ValueError(f"Cell {ref} is not a NumericalContent object.")
                    else:
                        raise ValueError(f"Undefined cell reference: {ref}")
                
                # Reemplazar referencias en la formula
                formula = re.sub(pattern, replace_reference, formula)
                
            except Exception as e:
                print(f"Error: {e}")
                return None
            """
            
            result = computeFormula(formula, cell_values)
            self.textualvalue = str(result)

            # Elimina la celda del conjunto en proceso
            #self.spreadsheet.processing.remove(self.coordinate)

            return result
        except Exception as e:
            print(f"Error al calcular la formula: {e}")
            self.textualvalue = None
            return None

    def getTextualValue(self):
        return self.getValue()

    def get_content(self):
        return f"Formula: {self.formula}"
    
    def get_formula(self):
        """Devuelve la fórmula original como texto."""
        return self.formula

    def getNumericalValue(self):
        return self.calculateFormula()
        
    def process_functions_formula(self, formula: str):
        """
        Procesa una fórmula buscando funciones y reemplazándolas por sus resultados en el mismo string.
        Procesa funciones anidadas evaluándolas de adentro hacia afuera.
        :param formula: La fórmula en formato string.
        :return: La fórmula con las funciones reemplazadas por los resultados.
        """
        # Patrón para encontrar funciones como SUMA(1,2), MIN(A1:A2), etc.
        function_pattern = re.compile(r"(\w+)\(([^()]*?)\)")  # Busca funciones más internas (sin paréntesis anidados)
        
        while True:
            # Encuentra las funciones más internas
            matches = list(function_pattern.finditer(formula))
            if not matches:
                break  # Si no hay más funciones, terminamos el procesamiento
            
            # Procesar las funciones desde el final hacia el principio
            for match in reversed(matches):
                function_name, args_str = match.groups()
                
                # Procesar referencias de rangos y celdas dentro de los argumentos
                args = []
                for arg in args_str.split(";"):
                    arg = arg.strip()
                    if ":" in arg:  # Es un rango
                        arg = self.process_references_cells(arg)  # Reemplaza el rango por sus valores
                    args.append(arg)
                
                # Convierte los argumentos en números (ya procesados los rangos)
                numeric_args = [float(arg) for arg in ";".join(args).split(";")]
                
                # Evalúa la función
                result = evaluate_function(function_name, numeric_args)
                
                # Reemplaza la función completa con su resultado en la fórmula
                formula = (
                    formula[:match.start()] +
                    str(result) +
                    formula[match.end():]
                )
        
        return formula


    
    def process_references_cells(self, formula: str):
         # Procesar rangos primero
        cellValues = self.spreadsheet.getCells() #test
        range_pattern = r"([A-Z]+[0-9]+):([A-Z]+[0-9]+)"
        for match in re.finditer(range_pattern, formula):
            coord1, coord2 = match.groups()  # Coordenadas del rango
            cell_range = getCellRange(coord1, coord2)  # Obtén las celdas del rango
            if not cell_range:
                raise ValueError(f"Invalid range: {coord1}:{coord2}")

            # Reemplazar el rango con valores separados por ';'
            values = []
            for cell_coord in cell_range:
                if cell_coord in cellValues and isinstance(cellValues[cell_coord], NumericalContent):
                    values.append(str(cellValues[cell_coord].getNumericalValue()))
                else:
                    raise ValueError(f"Cell {cell_coord} in range {coord1}:{coord2} is undefined or invalid.")
            
            # Construir el reemplazo
            replacement = ";".join(values)
            formula = formula.replace(f"{coord1}:{coord2}", replacement)

        # Procesar referencias individuales
        pattern = r"\b[A-Z]+[0-9]+\b"  # Coincide con referencias individuales de celdas
        def replace_reference(match):
            ref = match.group(0)
            if ref in cellValues and isinstance(cellValues[ref], NumericalContent):
                return str(cellValues[ref].getNumericalValue())
            else:
                raise ValueError(f"Undefined or invalid cell reference: {ref}")

        # Reemplazar las referencias individuales en la fórmula
        formula = re.sub(pattern, replace_reference, formula)

        return formula
    
    


    
class CircularDependencyException(Exception):
    """
    Exception raised when a circular dependency is detected in the spreadsheet.
    """
    def __init__(self, message="Circular dependency detected"):
        super().__init__(message)


def evaluate_function(function_name, args):
    """
    Simula la evaluación de una función (por ejemplo, SUMA, MIN).
    :param function_name: Nombre de la función a evaluar.
    :param args: Lista de argumentos de la función.
    :return: El resultado de la función.
    """
    if function_name == "SUMA":
        return sum(args)
    elif function_name == "MIN":
        return min(args)
    elif function_name == "MAX":
        return max(args)
    elif function_name == "PROMEDIO":
        return sum(args) / len(args)
    else:
        raise ValueError(f"Función {function_name} no soportada")
    
def getCellRange(coord1: str, coord2: str):
        """
        Returns a list of cell coordinates within a rectangular range.
        
        :param coord1: The top-left cell of the range (e.g., "A1").
        :param coord2: The bottom-right cell of the range (e.g., "B2").
        :return: A list of cell coordinates (e.g., ["A1", "A2", "B1", "B2"]).
        """
        # Extraer las columnas y las filas de las coordenadas
        col1, row1 = re.match(r"([A-Z]+)([0-9]+)", coord1).groups()
        col2, row2 = re.match(r"([A-Z]+)([0-9]+)", coord2).groups()

        # Convertir filas a enteros
        row1, row2 = int(row1), int(row2)

        # Ordenar para manejar rangos invertidos (por si coord1 y coord2 están desordenados)
        col_start, col_end = sorted([col1, col2])
        row_start, row_end = sorted([row1, row2])

        # Generar todas las columnas en el rango
        def generate_columns(start_col, end_col):
            cols = []
            current = start_col
            while current <= end_col:
                cols.append(current)
                # Incrementar la columna
                current = increment_column(current)
            return cols

        # Incrementar columna (e.g., "A" → "B", "Z" → "AA")
        def increment_column(col):
            col = list(col)
            i = len(col) - 1
            while i >= 0:
                if col[i] == 'Z':
                    col[i] = 'A'
                    i -= 1
                    if i < 0:
                        col.insert(0, 'A')
                else:
                    col[i] = chr(ord(col[i]) + 1)
                    break
            return ''.join(col)

        # Generar todas las celdas dentro del rango
        columns = generate_columns(col_start, col_end)
        coord_list = [f"{col}{row}" for col in columns for row in range(row_start, row_end + 1)]

        return coord_list