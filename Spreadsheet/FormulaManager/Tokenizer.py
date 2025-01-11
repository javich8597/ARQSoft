class Tokenizer:
    def __init__(self, formula: str):
        self.formula = formula
        self.tokens = []

    def tokenize(self):
        # Implementar la lógica de tokenización aquí
        self.tokens = self.formula.split()
        return self.tokens
