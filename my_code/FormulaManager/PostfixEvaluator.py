class PostfixEvaluator:
    def evaluatePostfix(self, postfixExpression):
        stack = []
        try:
            for token in postfixExpression:
                if token["type"] == "operand":
                    stack.append(token["value"])
                elif token["type"] == "operator":
                    b = stack.pop()
                    a = stack.pop()
                    if token["value"] == '+':
                        stack.append(a + b)
                    elif token["value"] == '-':
                        stack.append(a - b)
                    elif token["value"] == '*':
                        stack.append(a * b)
                    elif token["value"] == '/':
                        if b == 0:
                            raise EvaluationException("Division by zero.")
                        stack.append(a / b)
            return stack.pop()
        except Exception as e:
            raise EvaluationException(f"Error during evaluation: {str(e)}")

    def pushTokenToStack(self, stack, token):
        if token["type"] != "operand":
            raise InvalidContentsException("Only operands can be pushed to the stack.")
        stack.append(token["value"])

class EvaluationException(Exception):
    pass

class InvalidContentsException(Exception):
    pass
