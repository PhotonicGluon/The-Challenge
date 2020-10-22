"""
q14.py

Created on 2020-08-21
Updated on 2020-10-22

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
import math
from fractions import Fraction

from sympy import latex
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q14(Question):
    """
    Q14:
    Simultaneous equations involving a linear equation (a chord of a circle) and the equation of that circle.
    It is guaranteed that there are two unique solutions for x and y.
    """

    def calculations(self):
        # CONSTANTS
        x_range = [-40, 40]  # If `x_range` = [a, b] then a <= x <= b
        y_range = [-40, 40]  # If `y_range` = [p, q] then p <= y <= q

        # CALCULATIONS
        # Generate the solutions
        while True:
            # Randomly select two points
            point_a = (self.random.randint(x_range[0], x_range[1]), self.random.randint(y_range[0], y_range[1]))
            point_b = (self.random.randint(x_range[0], x_range[1]), self.random.randint(y_range[0], y_range[1]))

            # Check if both x-coordinates and both y-coordinates are different
            if not (point_a[0] != point_b[0] and point_a[1] != point_b[1]):
                pass
            else:
                break

        # Calculate the gradient of line AB
        gradient_of_ab = Fraction(point_a[1] - point_b[1], point_a[0] - point_b[0])

        # Calculate the y-intercept of the line AB
        intercept_of_ab = Fraction(point_a[1] - gradient_of_ab * point_a[0])

        # Calculate LCM of both values' denominators
        denominator_lcm = self.lcm(gradient_of_ab.denominator, intercept_of_ab.denominator)

        # Generate the equation of the line
        exp_in_x = latex(parse_expr(f"{denominator_lcm * gradient_of_ab} * x + {denominator_lcm * intercept_of_ab}"))
        exp_in_y = latex(parse_expr(f"{denominator_lcm} * y"))
        eqn_of_line_ab = exp_in_y + " = " + exp_in_x  # This is equation 1

        # Calculate the gradient of the perpendicular bisector of line AB
        gradient_of_perp_bisector = Fraction(-1, gradient_of_ab)

        # Generate the midpoint, M, of AB
        midpoint_of_ab = (Fraction(point_a[0] + point_b[0], 2), Fraction(point_a[1] + point_b[1], 2))

        # Generate the x-coordinate for the centre of the circle
        o_x = self.random.randint(x_range[0], x_range[1])

        # Calculate the y-coordinate for the centre O
        o_y = gradient_of_perp_bisector * o_x + (midpoint_of_ab[1] - gradient_of_perp_bisector * midpoint_of_ab[0])

        # Calculate the (radius^2) of the circle
        radius_squared = (o_x - point_a[0]) ** 2 + (o_y - point_a[1]) ** 2

        # Generate the equation of the circle
        circle_lhs = latex(parse_expr(f"(x - {o_x}) ** 2 + (y - {o_y}) ** 2"))
        circle_rhs = latex(parse_expr(str(radius_squared)))

        eqn_of_circle = circle_lhs + " = " + circle_rhs  # This is equation 2

        # Set the values of `self.question` and `self.answer`
        self.question = [eqn_of_line_ab, eqn_of_circle]
        self.answer = [point_a[0], point_b[0]]

    def generate_question(self):
        string = f"Solve for the <strong>values</strong> of $x$ in the following simultaneous equations " \
                 f"(Equation \\eqref{{q14:eqn1}} and Equation \\eqref{{q14:eqn2}}):"

        for i, q in enumerate(self.question):
            string += f"$$\\begin{{equation}}{q}\\label{{q14:eqn{i + 1}}}\\end{{equation}}"

        return string

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["$x_1=$", "$x_2=$"]

    @staticmethod
    def lcm(x, y):
        return abs(x * y) // math.gcd(x, y)


# DEBUG CODE
if __name__ == "__main__":
    question = Q14(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
