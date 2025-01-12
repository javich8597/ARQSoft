from .Content import Content
from FormulaManager.FormulaProcessing import FormulaProcessing

class FormulaContent(Content):
    def __init__(self, formula: str):
        super().__init__('formula', formula)
        self.formula = formula

    def getNumericalValue(self):
        return self.calculateFormula()

    def calculateFormula(self):
        try:
            formula_processor = FormulaProcessing(self.formula)
            self.textualvalue = formula_processor.evaluate()
            return float(self.textualvalue)
        except Exception as e:
            print(f"Error al calcular la fórmula: {e}")
            return 0

    def getTextualValue(self):
        return self.getValue()

    def get_content(self):
        return f"Fórmula: {self.formula}"
