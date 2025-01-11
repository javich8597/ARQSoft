from .Content import Content

class FormulaContent(Content):
    def __init__(self, formula: str):
        super().__init__('formula', formula)

    def getNumericalValue(self):
        # Retornar un valor numérico calculado en base a la fórmula
        return 0

    def getTextualValue(self):
        return self.getValue()

    def get_content(self):
        return f"Fórmula: {self.formula}"
