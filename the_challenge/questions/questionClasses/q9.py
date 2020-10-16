"""
q9.py

Created on 2020-08-21
Updated on 2020-10-16

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex, diff
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q9(Question):
    """
    Q9:
    Derivative of "special functions" (sin x, cos x, tan x, e^x, and ln x).
    """

    def calculations(self):
        # CONSTANTS
        no_functions_to_test = 3  # How many functions' derivatives should be tested?
        testable_functions = ["sin({} * x + {})", "cos({} * x + {})", "tan({} * x + {})", "exp({} * x + {})",
                              "log({} * x + {})"]

        # CALCULATIONS
        # Choose 3 functions to test
        functions_to_test = self.random.sample(testable_functions, k=no_functions_to_test)

        # Decide the "inner functions"' coefficients
        coefficients1 = [self.random.choice([self.random.randint(-9, -1), self.random.randint(1, 9)]),
                         self.random.choice([self.random.randint(-9, -1), self.random.randint(1, 9)])]
        coefficients2 = [self.random.choice([self.random.randint(-9, -1), self.random.randint(1, 9)]),
                         self.random.choice([self.random.randint(-9, -1), self.random.randint(1, 9)])]
        coefficients3 = [self.random.choice([self.random.randint(-9, -1), self.random.randint(1, 9)]),
                         self.random.choice([self.random.randint(-9, -1), self.random.randint(1, 9)])]

        # Form the expression to be differentiated
        self.question = parse_expr(
            (" + ".join(functions_to_test)).format(coefficients1[0], coefficients1[1], coefficients2[0],
                                                   coefficients2[1], coefficients3[0], coefficients3[1]))

        # Generate the differentiated expression
        self.answer = diff(self.question)

    def generate_question(self):
        return f"Differentiate the following with respect to $x$:$${latex(self.question).replace('log', 'ln')}$$"

    def generate_answer(self):
        return latex(self.answer).replace("log", "ln")

    def generate_input_fields_prefixes(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q9(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
