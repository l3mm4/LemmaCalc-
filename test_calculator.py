import unittest
from calc import evaluate_expression, format_result, variables


class CalculatorTestCase(unittest.TestCase):

    def setUp(self):
        variables.clear()

    def test_basic_operations(self):
        self.assertEqual(format_result(evaluate_expression("2 + 2", variables)), "4")
        self.assertEqual(format_result(evaluate_expression("5 - 3", variables)), "2")
        self.assertEqual(format_result(evaluate_expression("4 * 3", variables)), "12")
        self.assertEqual(format_result(evaluate_expression("10 / 2", variables)), "5.0")
        self.assertEqual(format_result(evaluate_expression("10 % 3", variables)), "1")

    def test_exponentiation_and_power(self):
        self.assertEqual(format_result(evaluate_expression("2 ** 3", variables)), "8")
        self.assertEqual(
            format_result(evaluate_expression("pow(2, 4)", variables)), "16"
        )

    def test_order_of_operations(self):
        self.assertEqual(
            format_result(evaluate_expression("2 + 3 * 4", variables)), "14"
        )
        self.assertEqual(
            format_result(evaluate_expression("(2 + 3) * 4", variables)), "20"
        )

    def test_advanced_functions(self):
        self.assertAlmostEqual(evaluate_expression("sqrt(16)", variables), 4.0)
        self.assertAlmostEqual(evaluate_expression("log(e)", variables), 1.0, places=6)
        self.assertAlmostEqual(evaluate_expression("log10(1000)", variables), 3.0)
        self.assertAlmostEqual(evaluate_expression("sin(0)", variables), 0.0, places=6)
        self.assertAlmostEqual(evaluate_expression("cos(0)", variables), 1.0, places=6)
        self.assertAlmostEqual(evaluate_expression("tan(0)", variables), 0.0, places=6)

    def test_constants(self):
        self.assertAlmostEqual(
            evaluate_expression("pi", variables), 3.14159265, places=6
        )
        self.assertAlmostEqual(evaluate_expression("e", variables), 2.7182818, places=6)

    def test_factorials(self):
        self.assertEqual(format_result(evaluate_expression("5!", variables)), "120")
        self.assertEqual(format_result(evaluate_expression("0!", variables)), "1")
        self.assertEqual(format_result(evaluate_expression("1!", variables)), "1")
        self.assertEqual(format_result(evaluate_expression("3 + 4!", variables)), "27")

    def test_invalid_factorials(self):
        with self.assertRaises(ValueError):
            evaluate_expression("(-1)!", variables)
        with self.assertRaises(ValueError):
            evaluate_expression("1.5!", variables)

    def test_variable_assignments(self):
        self.assertEqual(
            format_result(evaluate_expression("x = 2 + 3", variables)), "5"
        )
        self.assertEqual(format_result(evaluate_expression("x + 1", variables)), "6")
        self.assertEqual(
            format_result(evaluate_expression("y = x * 2", variables)), "10"
        )
        self.assertEqual(format_result(evaluate_expression("y", variables)), "10")

    def test_multiple_expressions(self):
        evaluate_expression("a = 4", variables)
        evaluate_expression("b = 2", variables)
        self.assertEqual(
            format_result(evaluate_expression("a * b + 4", variables)), "12"
        )

    def test_syntax_errors(self):
        with self.assertRaises(SyntaxError):
            evaluate_expression("2 + ", variables)
        with self.assertRaises(SyntaxError):
            evaluate_expression("()", variables)

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            evaluate_expression("1 / 0", variables)

    def test_unknown_function(self):
        with self.assertRaises(NameError):
            evaluate_expression("sinn(0)", variables)

    def test_implicit_multiplication(self):
        self.assertEqual(format_result(evaluate_expression("3(2+1)", variables)), "9")
        self.assertEqual(
            format_result(evaluate_expression("2pi", variables)),
            format_result(2 * evaluate_expression("pi", variables)),
        )
        self.assertEqual(
            format_result(evaluate_expression("e3", variables)),
            format_result(evaluate_expression("e", variables) * 3),
        )

    def test_formatting_large_numbers(self):
        self.assertEqual(
            format_result(evaluate_expression("1000000 + 2500000", variables)),
            "3,500,000",
        )
        self.assertEqual(
            format_result(evaluate_expression("1000000 * 1000", variables)),
            "1,000,000,000",
        )

    def test_nested_parentheses_and_precedence(self):
        self.assertEqual(
            format_result(evaluate_expression("((2 + 3) * (4 + 1)) / 5", variables)),
            "5.0",
        )

    def test_combined_variables_and_constants(self):
        evaluate_expression("r = 3", variables)
        self.assertEqual(
            format_result(evaluate_expression("2 * pi * r", variables)),
            format_result(2 * 3.14159265 * 3),
        )


if __name__ == "__main__":
    unittest.main()
