from contentHandler.models.Content import Content
from code.FormulaManager.FormulaProcessing import computeFormula
#from code.Spreadsheet import Spreadsheet
#from code.DependencyManager import DependencyManager

class FormulaContent(Content):
    def __init__(self, formula: str, dependencyManager):
        super().__init__('formula', formula)
        self.formula = formula
        self.dependencyManager = dependencyManager
        

    def calculateFormula(self):
        try:
            cell_values = self.dependencyManager.getCellValues()
            result = computeFormula(self.formula, cell_values)
            self.textualvalue = str(result)
            return result
        except Exception as e:
            print(f"Error al calcular la fórmula: {e}")
            self.textualvalue = None
            return None

    def getTextualValue(self):
        return self.getValue()

    def get_content(self):
        return f"Fórmula: {self.formula}"

    def getNumericalValue(self):
        return self.calculateFormula()