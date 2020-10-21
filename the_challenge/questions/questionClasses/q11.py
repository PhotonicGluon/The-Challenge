"""
q11.py

Created on 2020-08-21
Updated on 2020-10-21

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex, integrate
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.misc import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q11(Question):
    """
    Q12:
    Definite integral of a polynomial.
    """

    def calculations(self):
        # CONSTANTS
        no_terms = 3  # How many terms should there be in the polynomial that the user has to integrate?
        power_range = [1, 5]  # If `power_range` = [a, b] then a <= p <= b where p is the degree of the term
        integral_limits = [-10, 10]  # If `integral_limits` = [a, b] then the limits of the integral are a to b.

        # CALCULATIONS
        # Determine the degree of the polynomial
        deg = self.random.randint(no_terms, power_range[1])

        # Generate the pre-integral terms
        terms = []
        for i in range(no_terms):
            # Generate the coefficient
            coefficient = self.random.randint(1, 9)

            # Generate the term
            term = f"{coefficient} * x ** {deg - i}"

            # Append the term to the terms
            terms.append(term)

        # Sum all terms up
        polynomial = parse_expr(" + ".join(terms))

        # Calculate the integral of the polynomial
        integral = integrate(polynomial)

        # Calculate the definite integral
        a = self.random.randint(integral_limits[0], integral_limits[1] - 1)  # Lower limit
        b = self.random.randint(a + 1, integral_limits[1])  # Upper limit

        ans = mathematical_round(float(integral.subs("x", b) - integral.subs("x", a)), 3)

        # Set the values of `self.question` and `self.answer`
        self.question = [latex(polynomial), a, b]
        self.answer = ans

    def generate_question(self):
        string = f"Calculate: $$\\int_{{{self.question[1]}}}^{{{self.question[2]}}}\\left({self.question[0]}\\right)" \
                 f"\\:{{dx}}$$"

        return string

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q11(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
