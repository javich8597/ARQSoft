import re 
class PostfixGenerator:
    def convertToOperandsAndOperators(self, tokens):
        categorized = []
        for token in tokens:
            if token.isdigit() or re.match(r"\d+\.\d+", token):
                categorized.append({"type": "operand", "value": float(token)})
            elif token in "+-*/()=":
                categorized.append({"type": "operator", "value": token})
            else:
                categorized.append({"type": "variable", "value": token})
        return categorized

    def reorderTokens(self, tokens):
        output = []
        stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}

        for token in tokens:
            if token["type"] == "operand" or token["type"] == "variable":
                output.append(token)
            elif token["type"] == "operator":
                while stack and precedence[stack[-1]["value"]] >= precedence[token["value"]]:
                    output.append(stack.pop())
                stack.append(token)
            elif token["value"] == '(':
                stack.append(token)
            elif token["value"] == ')':
                while stack and stack[-1]["value"] != '(':
                    output.append(stack.pop())
                stack.pop()

        while stack:
            output.append(stack.pop())

        return output
