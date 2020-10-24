"""
q13.py

Created on 2020-08-21
Updated on 2020-10-24

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex, integrate, expand
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q13(Question):
    """
    Q13:
    Combination of derivatives and solving of cubic equation.
    It is guaranteed that there will be at least one "trivial" solution, and that all solutions are integers.
    """

    def calculations(self):
        # CONSTANTS
        non_trivial_solutions_ranges = [3, 20]  # If the range is [a, b] then a <= x <= b where x is a root

        # CALCULATIONS
        # Generate the three (expected) solutions
        sol2_and_sol3_list = [x for x in range(non_trivial_solutions_ranges[0], non_trivial_solutions_ranges[1])] + \
                             [-x for x in range(non_trivial_solutions_ranges[0], non_trivial_solutions_ranges[1])]

        sol1 = self.random.choice([-1, 1, -2, 2])  # These are the "trivial" solutions
        sol2, sol3 = self.random.sample(sol2_and_sol3_list, k=2)

        self.answer = [sol1, sol2, sol3]

        # Form the factorised version of the cubic equation
        cubic_factorised = parse_expr(f"(x - {sol1}) * (x - {sol2}) * (x - {sol3})")

        # Expand the cubic equation
        cubic_eqn = expand(cubic_factorised)

        # Take the integral of the cubic equation
        integral_eqn = latex(integrate(cubic_eqn) + self.random.randint(-1000, 1000))
        self.question = integral_eqn

    def generate_question(self):
        return "Solve for the <strong>values</strong> of $x$ in the equation $$\\frac{\mathrm{d}}{\mathrm{d}" \
               f"x}}\\left({self.question}\\right) = 0$$"

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["$x_1=$", "$x_2=$", "$x_3=$"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q13(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
