# calculator/tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_power_of_simple(self):
        result = self.calculator.evaluate("2 ^ 3")
        self.assertEqual(result, 8)

    def test_power_of_precedence_multiplication(self):
        result = self.calculator.evaluate("2 ^ 2 * 8 - 3")
        self.assertEqual(result, 29)

    def test_power_of_precedence_division(self):
        result = self.calculator.evaluate("4 * 2 ^ 3 / 2")
        self.assertEqual(result, 16)

    def test_modulo_simple(self):
        result = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)

    def test_modulo_zero_remainder(self):
        result = self.calculator.evaluate("9 % 3")
        self.assertEqual(result, 0)

    def test_modulo_precedence_multiplication(self):
        result = self.calculator.evaluate("10 + 2 % 3 * 5") # 10 + (2 % 3) * 5 = 10 + 2 * 5 = 20
        self.assertEqual(result, 20)

    def test_sqrt_simple(self):
        result = self.calculator.evaluate("sqrt 9")
        self.assertEqual(result, 3)

    def test_sqrt_zero(self):
        result = self.calculator.evaluate("sqrt 0")
        self.assertEqual(result, 0)

    def test_sqrt_decimal(self):
        result = self.calculator.evaluate("sqrt 2.25")
        self.assertEqual(result, 1.5)

    def test_sqrt_expression(self):
        result = self.calculator.evaluate("sqrt ( 4 + 5 )") # sqrt(9) = 3
        self.assertEqual(result, 3)

    def test_sqrt_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("sqrt -9")

    def test_sqrt_precedence(self):
        result = self.calculator.evaluate("2 + sqrt 9 * 2") # 2 + 3 * 2 = 8
        self.assertEqual(result, 8)


if __name__ == "__main__":
    unittest.main()
