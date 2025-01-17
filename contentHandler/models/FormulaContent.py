from contentHandler.models.Content import Content
from my_code.FormulaManager.FormulaProcessing import computeFormula

class FormulaContent(Content):
    def __init__(self, formula: str, spreadsheet) -> None:
        super().__init__('formula', formula)
        self.formula = formula
        self.spreadsheet = spreadsheet
        
        #self.dependencyManager = dependencyManager

    def getNumericalValue(self) -> float:
        return self.calculateFormula()
    
    def get_content(self):
        return f"Fórmula: {self.formula}"

    def calculateFormula(self):
        try:
            #cell_values = self.dependencyManager.getCellValues()
            cell_values = self.spreadsheet.getCells()
            result = computeFormula(self.formula, cell_values)
            self.textualvalue = str(result)
            return result
        except Exception as e:
            print(f"Error al calcular la fórmula: {e}")
            self.textualvalue = None
            return None