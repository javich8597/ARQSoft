from contentHandler.models.Content import Content
from my_code.FormulaManager.FormulaProcessing import computeFormula

class FormulaContent(Content):
    def __init__(self, formula: str, spreadsheet) -> None:
        if not spreadsheet:
            raise ValueError("JAVI: A valid spreadsheet reference is required.")
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
            result = computeFormula(self.formula, cell_values)
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
    
class CircularDependencyException(Exception):
    """
    Exception raised when a circular dependency is detected in the spreadsheet.
    """
    def __init__(self, message="Circular dependency detected"):
        super().__init__(message)
