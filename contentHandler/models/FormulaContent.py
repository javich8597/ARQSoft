from contentHandler.models.Content import Content
import re

class FormulaContent(Content):
    def __init__(self, formula: str, dependencyManager):
        super().__init__('formula', formula)
        self.formula = formula
        self.dependencyManager = dependencyManager
        
    def extractDependencies(self):
        """
        Extrae las dependencias de la fórmula (referencias a otras celdas).

        :return: Lista de coordenadas de celdas referenciadas en la fórmula.
        """
        # Expresión regular para identificar celdas (e.g., A1, B2, Z99)
        pattern = r"[A-Z]+[0-9]+"
        dependencies = re.findall(pattern, self.formula)
        return dependencies

    def calculateFormula(self, cell_values):
        try:
            from my_code.FormulaManager.FormulaProcessing import computeFormula
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