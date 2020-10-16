"""
q7.py

Created on 2020-08-21
Updated on 2020-10-16

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.misc import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q7(Question):
    """
    Q7:
    Simple logarithm-cum-modulus equation.
    """

    def calculations(self):
        # Generate the constants' values
        a = self.random.randint(2, 9)
        b = self.random.choice([self.random.randint(1, 9), -self.random.randint(1, 9)])
        c = self.random.randint(2, 10)
        d = self.random.randint(2, 9)
        e = self.random.randint(-9, 9)
        f = self.random.randint(1, 10)

        # Generate the equation
        self.question = latex(parse_expr(f"{a} * Abs({b} * log({d}*x, {c}) + {e}) - {f}")).replace("log", "ln") + " = 0"

        # Generate the answer
        ans1 = mathematical_round(float(parse_expr(f"1/{d} * {c}**((-{f}/{a} - {e}) / {b})")), 3)
        ans2 = mathematical_round(float(parse_expr(f"1/{d} * {c}**(({f}/{a} - {e}) / {b})")), 3)

        self.answer = [ans1, ans2]

    def generate_question(self):
        return f"Solve for the <strong>values</strong> of $x$:$${self.question}$$"

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["$x_1=$", "$x_2=$"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q7(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
