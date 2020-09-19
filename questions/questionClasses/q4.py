"""
q4.py

Created on 2020-08-21
Updated on 2020-09-19

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.

Todo:
    - Find a way to ensure that the user actually expanded/factorised the question's expressions.
"""

# IMPORTS
from sympy import latex, symbols
from sympy.parsing.sympy_parser import parse_expr

from questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q4(Question):
    """
    Q4:
    Factorising OR Expanding of some identities.
    """

    def __init__(self, seed_value=None):
        super().__init__(seed_value)
        self.factorise_or_simplify = None

    def calculations(self):
        # CONSTANTS
        identities = ["A**3+B**3", "A**3-B**3", "A**2+2*A*B+B**2", "A**2-2*A*B+B**2", "A**2-B**2"]
        factorised_version = ["(A+B)*(A**2-A*B+B**2)", "(A-B)*(A**2+A*B+B**2)", "(A+B)**2", "(A-B)**2", "(A+B) * (A-B)"]

        # CALCULATIONS
        # Define the variables
        a, b = symbols("A B")
        w, x, y, z = symbols("w x y z")

        # Decide what to do for this question
        self.factorise_or_simplify = "factorise" if self.random.randint(0, 1) == 0 else "simplify"

        # Generate the expressions & get their indexes
        if self.factorise_or_simplify == "factorise":
            exp1, exp2 = self.random.sample(identities, 2)  # One is the identity itself
            index1, index2 = identities.index(exp1), identities.index(exp2)

        else:  # Simplify
            exp1, exp2 = self.random.sample(factorised_version, 2)  # Another is the factorised version
            index1, index2 = factorised_version.index(exp1), factorised_version.index(exp2)

        # Parse the expressions
        exp1 = parse_expr(exp1)
        exp2 = parse_expr(exp2)

        # Substitute some multiples of x and y as A and B
        a1 = self.random.randint(2, 9) * w
        b1 = self.random.randint(2, 9) * x
        a2 = self.random.randint(2, 9) * y
        b2 = self.random.randint(2, 9) * z

        exp1 = exp1.subs(a, a1).subs(b, b1)
        exp2 = exp2.subs(a, a2).subs(b, b2)

        # Generate the question and answer
        if self.factorise_or_simplify == "factorise":
            self.question = [latex(exp1 * exp2)]
            ans1 = parse_expr(factorised_version[index1]).subs(a, a1).subs(b, b1)
            ans2 = parse_expr(factorised_version[index2]).subs(a, a2).subs(b, b2)

        else:
            self.question = [latex(exp1), latex(exp2)]
            ans1 = parse_expr(identities[index1]).subs(a, a1).subs(b, b1)
            ans2 = parse_expr(identities[index2]).subs(a, a2).subs(b, b2)

        self.answer = ans1 * ans2

    def generate_question(self):
        if self.factorise_or_simplify == "factorise":
            string = f"Factorise the following expression <strong>completely</strong>:$${self.question[0]}$$"
        else:
            string = f"Expand the following expressions, and then write the product of Equation \\eqref{{q4:eqn1}} " \
                     f"and Equation \\eqref{{q4:eqn2}} as your answer:" \
                     f"$$\\begin{{equation}}{self.question[0]}\\label{{q4:eqn1}}\\end{{equation}}$$" \
                     f"$$\\begin{{equation}}{self.question[1]}\\label{{q4:eqn2}}\\end{{equation}}$$"

        return string

    def generate_answer(self):
        return latex(self.answer)

    def answer_input_fields_prefix(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q4(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
