"""
q11.py

Created on 2020-08-21
Updated on 2020-10-16

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex, symbols, integrate, sin, cos, sec, exp

from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q11(Question):
    """
    Q11:
    Integral of (ax + b)^n for any rational n (including negative n), sin(ax + b), cos(ax + b), sec(x)^2 and/or
    e^(ax + b), together with constant multiples, sums and differences.
    """

    def calculations(self):
        # CONSTANTS
        no_functions_to_test = 3  # How many functions' derivatives should be tested?
        a, b, n, k, x = symbols("A B N K x")
        testable_functions = [k * (a * x + b) ** n, k * sin(a * x + b), k * cos(a * x + b), k * sec(x) ** 2,
                              k * exp(a * x + b)]

        # CALCULATIONS
        # Choose the functions to test
        functions_to_test = self.random.sample(testable_functions, k=no_functions_to_test)

        # Assign the constants for each of the functions
        assigned_functions = []
        for func in functions_to_test:
            # Substitute values for A, B, N and K
            val_a = self.random.randint(1, 9)
            val_b = self.random.randint(1, 9)
            val_n = self.random.choice([self.random.randint(1, 9), -self.random.randint(1, 9)])
            val_k = self.random.choice([self.random.randint(1, 9), -self.random.randint(1, 9)])
            assigned_function = func.subs(a, val_a).subs(b, val_b).subs(n, val_n).subs(k, val_k)

            # Append the formed function to all the other functions
            assigned_functions.append(assigned_function)

        # Sum all the functions together
        expression_to_integrate = sum(assigned_functions)

        # Generate the integral of the expression
        integral = integrate(expression_to_integrate)

        # Set the values of `self.question` and `self.answer`
        self.question = latex(expression_to_integrate)
        self.answer = integral

    def generate_question(self):
        string = f"Integrate the following with respect to $x$, leaving out the constant of integration ($C$) in " \
                 f"your answer:$${self.question}$$"

        return string

    def generate_answer(self):
        return latex(self.answer)

    def generate_input_fields_prefixes(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q11(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
