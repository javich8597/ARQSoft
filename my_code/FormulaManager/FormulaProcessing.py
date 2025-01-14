import re
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
            elif token in ["SUMA", "PROMEDIO", "MIN", "MAX"]:
                categorized.append({"type": "function", "value": token})
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
            if token["type"] in ["operand", "variable"]:
                output.append(token)
            elif token["type"] == "operator":
                while stack and precedence[stack[-1]["value"]] >= precedence[token["value"]]:
                    output.append(stack.pop())
                stack.append(token)
            elif token["type"] == "function":
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

    def evaluatePostfix(self, postfixExpression, cellValues):
        """
        Evaluates the postfix expression and returns the result.

        :param postfixExpression: A list of tokens in postfix notation.
        :param cellValues: A dictionary containing cell values for variables.
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
                elif token["type"] == "variable":
                    if token["value"] not in cellValues:
                        raise EvaluationException(f"Cell {token['value']} is undefined.")
                    stack.append(cellValues[token["value"]])
                elif token["type"] == "function":
                    if token["value"] == "MAX":
                        args = []
                        while stack and isinstance(stack[-1], (int, float)):
                            args.append(stack.pop())
                        stack.append(max(args))
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


class EvaluationException(Exception):
    """
    Exception raised during evaluation of a postfix expression.
    """
    pass


def computeFormula(formula: str, cellValues: dict):
    """
    Computes the result of a formula by tokenizing, parsing, converting to postfix,
    and evaluating it.

    :param formula: The formula string to compute.
    :param cellValues: A dictionary containing cell values for variables.
    :return: The computed result.
    """
    try:
        tokenizer = Tokenizer()
        parser = Parser()
        postfix_generator = PostfixGenerator()
        evaluator = PostfixEvaluator()

        # Step 1: Tokenize the formula
        tokens = tokenizer.tokenize(formula)

        # Step 2: Parse the tokens to check syntax
        parser.parse(tokens)

        # Step 3: Convert tokens to postfix notation
        categorized_tokens = postfix_generator.convertToOperandsAndOperators(tokens)
        postfix_tokens = postfix_generator.reorderTokens(categorized_tokens)

        # Step 4: Evaluate the postfix expression
        result = evaluator.evaluatePostfix(postfix_tokens, cellValues)
        return result

    except (TokenizerException, InvalidFormulaSintaxException, EvaluationException) as e:
        print(f"Error computing formula: {str(e)}")
        return None
