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
        try:
            # Remove '=' at the start of the formula if it exists
            if formula.startswith("="):
                formula = formula[1:]

            pattern = r"[A-Za-z]+\d+|\d+\.\d+|\d+|[+\-*/()=]"
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
            elif token in "+-*/":
                categorized.append({"type": "operator", "value": token})
            elif token == "(" or token == ")":
                # Parenthesis are categorized as special operators
                categorized.append({"type": "parenthesis", "value": token})
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
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

        for token in tokens:
            if token["type"] in ["operand", "variable"]:
                # Operand add to output
                output.append(token)
            elif token["type"] == "operator":
                # Process operators
                while stack and stack[-1]["type"] == "operator" and precedence.get(stack[-1]["value"], 0) >= precedence.get(token["value"], 0):
                    output.append(stack.pop())
                stack.append(token)
            elif token["value"] == '(':
                # Parenthesis are pushed to the stack
                stack.append(token)
            elif token["value"] == ')':
                # Process until '('
                while stack and stack[-1]["value"] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise InvalidFormulaSintaxException("Mismatched parentheses: no opening parenthesis.")
                stack.pop()  

        # Remove '(' from stack
        while stack:
            if stack[-1]["value"] == '(':
                raise InvalidFormulaSintaxException("Mismatched parentheses: no closing parenthesis.")
            output.append(stack.pop())

        # Remove parenthesis tokens if there are any
        output = [token for token in output if token["value"] not in ['(', ')']]

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
                    if len(stack) < 2:
                        raise EvaluationException(f"Insufficient operands for operator '{token['value']}'")
                    b = stack.pop()
                    a = stack.pop()
                    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                        raise EvaluationException(f"Operands must be numbers, got {type(a)} and {type(b)}")
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
            if len(stack) != 1:
                raise EvaluationException(f"Invalid postfix expression: stack={stack}")
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
