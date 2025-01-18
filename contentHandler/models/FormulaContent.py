from contentHandler.models.Content import Content
from my_code.FormulaManager.FormulaProcessing import computeFormula

class FormulaContent(Content):
    def __init__(self, formula: str, spreadsheet) -> None:
        if not spreadsheet:
            raise ValueError("JAVI: A valid spreadsheet reference is required.")
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
            tokens = computeFormula(self.formula, cell_values)
            for token in tokens:
                if token["type"] == "variable" and token["value"] not in cell_values:
                    raise KeyError(f"JAVI: Missing value for cell: {token['value']}")

            result = computeFormula(self.formula, cell_values)
            self.textualvalue = str(result)
            return result
        except Exception as e:
            print(f"Error al calcular la fórmula: {e}")
            self.textualvalue = None
            return None