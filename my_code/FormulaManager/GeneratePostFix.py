class GeneratePostFix:
    def __init__(self, expression):
        self.expression = expression

    def to_postfix(self):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output = []
        stack = []

        for char in self.expression:
            if char.isalnum():
                output.append(char)
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != '(' and precedence[char] <= precedence[stack[-1]]:
                    output.append(stack.pop())
                stack.append(char)

        while stack:
            output.append(stack.pop())

        return ''.join(output)
