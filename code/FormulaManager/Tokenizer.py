class Tokenizer:
    def __init__(self, formula: str):
        self.formula = formula
        self.tokens = []

    def tokenize(self):
        import re
        pattern = r"[A-Za-z]+\d+|\d+\.\d+|\d+|[+\-*/()=]|SUMA|PROMEDIO|MIN|MAX"
        self.tokens = re.findall(pattern, self.formula)
        if not self.tokens:
            raise TokenizerException("No valid tokens found.")
        return self.tokens

class TokenizerException(Exception):
    pass
