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

            #BUSCAR FUNCIONES EN LA FORMULA Y APLICARLAS AQUI
            formula = self.process_formula()
            

            #OJO ESTO TIENE QUE SER DESPUES DE HACER TODAS LAS FUNCIONES, SI NO PERDEMOS LOS RANGOS DE CELDAS POR EJEMPLO
            #Arreglamos la expresion de la formula primero 
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

    def getNumericalValue(self):
        return self.calculateFormula()
        
    def process_formula(self):
        """
        Procesa una fórmula buscando funciones y reemplazándolas por sus resultados en el mismo string.
        :param formula: La fórmula en formato string.
        :return: La fórmula con las funciones reemplazadas por los resultados.
        """
        formula = self.formula
        # Patrón para encontrar funciones como SUMA(1,2), MIN(3,4), etc.
        if not re.search(r"\w+\(.*\)", formula):
        # Si no hay funciones, no hace falta procesamiento adicional
            return formula
        
        function_pattern = re.compile(r"(\w+)\((.*?)\)")
        # Busca todas las funciones en la fórmula
        matches = function_pattern.findall(formula)
        
        for match in matches:
            function_name, args_str = match
            # Convierte los argumentos en una lista de números
            args = [float(arg.strip()) for arg in args_str.split(";")]
            # Evalúa la función
            result = evaluate_function(function_name, args)
            # Reemplaza la función con su resultado numérico en la fórmula
            formula = formula.replace(f"{function_name}({args_str})", str(result))
        self.formula = formula  # Actualiza la fórmula en el objeto
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