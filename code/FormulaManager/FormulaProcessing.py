class Tokenizer:
    """
    Tokenizes formulas into a sequence of tokens.
    """

    def tokenize(self, formula: str):
        """
        Splits the argument formula into a sequence of tokens.

        :param formula: The formula string to tokenize.
        :return: A list of tokens.

        Exceptional Situations:
            - TokenizerException
        """
        import re
        try:
            pattern = r"[A-Za-z]+\d+|\d+\.\d+|\d+|[+\-*/()=]|SUMA|PROMEDIO|MIN|MAX"
            tokens = re.findall(pattern, formula)
            if not tokens:
                raise TokenizerException("No valid tokens found.")
            return tokens
        except Exception as e:
            raise TokenizerException(f"Error tokenizing formula: {str(e)}")


class TokenizerException(Exception):
    """
    Exception raised for errors during tokenization.
    """
    pass


class Parser:
    """
    Parses sequences of tokens to check syntax.
    """

    def parse(self, tokens):
        """
        Checks that the sequence meets syntactical rules.

        :param tokens: A list of tokens to parse.
        :return: True if syntax is valid.

        Exceptional Situations:
            - InvalidFormulaSintaxException
        """
        try:
            # Simplified syntax validation example
            if not tokens:
                raise InvalidFormulaSintaxException("Token list is empty.")
            # Example: Validate parentheses balance
            stack = []
            for token in tokens:
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
    """
    Exception raised for invalid formula syntax.
    """
    pass


class PostfixGenerator:
    """
    Converts tokens into postfix notation.
    """

    def convertToOperandsAndOperators(self, tokens):
        """
        Converts string tokens into categorized operands or operators.

        :param tokens: A list of tokens to categorize.
        :return: A list of categorized tokens.
        """
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
        """
        Reorders tokens in infix notation to postfix notation using the Shunting Yard algorithm.

        :param tokens: A list of tokens in infix notation.
        :return: A list of tokens in postfix notation.
        """
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


class PostfixEvaluator:
    """
    Evaluates expressions in postfix notation.
    """

    def evaluatePostfix(self, postfixExpression):
        """
        Evaluates the postfix expression and returns the result.

        :param postfixExpression: A list of tokens in postfix notation.
        :return: The evaluated result.

        Exceptional Situations:
            - EvaluationException
            - InvalidFormulaSintaxException
            - InvalidContentsException
        """
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
        """
        Pushes valid operands to the stack.

        :param stack: The stack to push the token onto.
        :param token: The token to push.
        """
        if token["type"] != "operand":
            raise InvalidContentsException("Only operands can be pushed to the stack.")
        stack.append(token["value"])


class EvaluationException(Exception):
    """
    Exception raised during evaluation of a postfix expression.
    """
    pass


class InvalidContentsException(Exception):
    """
    Exception raised when invalid contents are encountered.
    """
    pass

