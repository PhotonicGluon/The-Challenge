"""
q6.py

Created on 2020-08-21
Updated on 2020-09-19

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
import math

from sympy import latex
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q6(Question):
    """
    Q6:
    Solve an equation involving surds.
    """

    def calculations(self):
        # Determine the constants a, b, c and d
        a = self.random.randint(1, 10)
        b = self.random.randint(1, 10)
        c = self.random.randint(1, 100)
        d = self.random.randint(math.ceil(math.sqrt(c)), 20)

        # Form the surd equation
        self.question = latex(parse_expr(f"sqrt({a} * sqrt({b} * x) + {c}) - {d}")) + " = 0"

        # Calculate the answer
        self.answer = round((((d ** 2 - c) / a) ** 2) / b, 3)

    def generate_question(self):
        return f"Solve for $x$:$${self.question}$$"

    def generate_answer(self):
        return self.answer

    def answer_input_fields_prefix(self):
        return ["$x=$"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q6(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
