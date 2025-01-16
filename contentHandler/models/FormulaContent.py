from contentHandler.models.Content import Content
from my_code.FormulaManager.FormulaProcessing import computeFormula

class FormulaContent(Content):
    def __init__(self, formula: str, spreadsheet) -> None:
        super().__init__('formula', formula)
        self.formula = formula
        self.spreadsheet = spreadsheet
        

    def calculateFormula(self):
        try:
            cell_values = self.spreadsheet.getCells() #test
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