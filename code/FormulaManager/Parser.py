class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        try:
            if not self.tokens:
                raise InvalidFormulaSintaxException("Token list is empty.")
            stack = []
            for token in self.tokens:
                if token == '(':
                    stack.append(token)
                elif token == ')':
                    if not stack:
                        raise InvalidFormulaSintaxException("Unmatched closing parenthesis.")
                    stack.pop()
            if stack:
                raise InvalidFormulaSintaxException("Unmatched opening parenthesis.")
            return True
        except Exception as e:
            raise InvalidFormulaSintaxException(f"Syntax error: {str(e)}")

class InvalidFormulaSintaxException(Exception):
    pass
