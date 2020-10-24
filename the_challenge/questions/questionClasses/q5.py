"""
q5.py

Created on 2020-10-05
Updated on 2020-10-24

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex, symbols

from the_challenge.misc.mathematicalRounding import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q5(Question):
    """
    Q5:
    Application of the Polynomial Remainder Theorem on a given polynomial.
    """

    def calculations(self):
        # CONSTANTS
        no_terms_in_polynomial = 8  # The number of terms inside the polynomial

        # CALCULATIONS
        # Set up variables
        x = symbols("x")

        # Generate polynomial
        polynomial = 0 * x  # Make it like an expression so that the IDEs will not complain
        for degree in range(no_terms_in_polynomial):  # The first term will be the constant term
            # Generate coefficients of the term
            coefficient = self.random.choice([self.random.randint(1, 9), -self.random.randint(1, 9)])

            # Generate the term
            term = coefficient * x ** degree

            # Add the term to the polynomial
            polynomial += term

        # Generate the linear expression for the polynomial to be divided by
        coefficient1 = self.random.choice([self.random.randint(1, 9), -self.random.randint(1, 9)])
        coefficient2 = self.random.choice([self.random.randint(1, 9), -self.random.randint(1, 9)])
        linear = coefficient1 * x + coefficient2

        # Generate the remainder when the polynomial is divided by the linear expression
        remainder = polynomial.subs(x, -coefficient2 / coefficient1)

        # Define `self.question` and `self.answer`
        self.question = [latex(polynomial), latex(linear)]
        self.answer = remainder

    def generate_question(self):
        string = f"State the remainder when the polynomial $$\\mathrm{{P}}(x) = {self.question[0]}$$ is divided by " \
                 f"the linear function $\\mathrm{{L}}(x) = {self.question[1]}$."
        return string

    def generate_answer(self):
        return mathematical_round(float(self.answer), 3)

    def generate_input_fields_prefixes(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q5(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
