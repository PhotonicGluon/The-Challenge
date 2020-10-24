"""
q8.py

Created on 2020-08-21
Updated on 2020-10-24

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
import math

from sympy import latex
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.misc import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q8(Question):
    """
    Q8:
    Solve an equation involving two nested surds.
    """

    def calculations(self):
        # Determine the constants a, b, c and d
        a = self.random.randint(2, 10)
        b = self.random.choice([2, 3, 5, 6, 7, 8, 10])  # Remove any perfect squares
        c = self.random.randint(2, 100)
        d = self.random.randint(math.ceil(math.sqrt(c)), 20)

        # Form the surd equation
        self.question = latex(parse_expr(f"sqrt({a} * sqrt({b} * x) + {c}) - {d}")) + " = 0"

        # Calculate the answer
        self.answer = mathematical_round((((d ** 2 - c) / a) ** 2) / b, 3)

    def generate_question(self):
        return f"Solve for the value of $x$ in the equation $${self.question}$$"

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["$x=$"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q8(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
