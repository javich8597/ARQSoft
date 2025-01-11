class Formula:
    def __init__(self, expression: str):
        self.expression = expression

    def evaluate(self):
        # Implementar la lógica de evaluación de la fórmula aquí
        return eval(self.expression)
