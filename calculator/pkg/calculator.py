# calculator/pkg/calculator.py

import math


class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "^": lambda a, b: a ** b,  # Add power-of operator
            "%": lambda a, b: a % b,  # Add modulo operator
            "sqrt": lambda a: math.sqrt(a),  # Add square root operator (unary)
            "nrt": lambda a, b: a ** (1/b), # Add nth root operator (binary)
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "%": 2,  # Same precedence as multiply/divide
            "^": 3,  # Higher precedence for power-of
            "sqrt": 4, # Highest precedence for sqrt as it's a unary operator
            "nrt": 3, # Same precedence as power-of, it's also a power operation.
        }
        self.unary_operators = ["sqrt"]

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        tokens = []
        current_token = ""
        for char in expression:
            if char in "() ":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                if char != " ":
                    tokens.append(char)
            else:
                current_token += char
        if current_token:
            tokens.append(current_token)
        return tokens

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if operators and operators[-1] == "(":
                    operators.pop() # Pop the '('
                else:
                    raise ValueError("Mismatched parentheses")
            elif token in self.operators:
                if token in self.unary_operators:
                    operators.append(token)
                else: # Binary operator
                    while (
                        operators
                        and operators[-1] in self.operators
                        and operators[-1] not in self.unary_operators # Ensure we don't pop unary operators for binary ops prematurely
                        and self.precedence.get(operators[-1], 0) >= self.precedence.get(token, 0)
                    ):
                        self._apply_operator(operators, values)
                    operators.append(token)
            else: # It's a number (operand)
                try:
                    values.append(float(token))
                    # Check for unary operators *immediately* after an operand is pushed.
                    # This ensures `sqrt 9` evaluates `sqrt` as soon as `9` is available.
                    while operators and operators[-1] in self.unary_operators:
                        self._apply_operator(operators, values)
                except ValueError:
                    raise ValueError(f"invalid token: {token}")
            i += 1

        while operators:
            if operators[-1] == "(":
                raise ValueError("Mismatched parentheses")
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        
        if operator in self.unary_operators:
            if len(values) < 1:
                raise ValueError(f"not enough operands for unary operator {operator}")
            operand = values.pop()
            values.append(self.operators[operator](operand))
        else:
            # Binary operators
            if len(values) < 2:
                raise ValueError(f"not enough operands for operator {operator}")

            b = values.pop()
            a = values.pop()
            values.append(self.operators[operator](a, b))
