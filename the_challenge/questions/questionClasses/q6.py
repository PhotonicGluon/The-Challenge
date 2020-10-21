"""
q6.py

Created on 2020-08-21
Updated on 2020-10-21

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
import itertools
import math
from fractions import Fraction

from sympy import latex
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.misc import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q6(Question):
    """
    Q6:
    Identify, using the discriminant, which of the three quadratic equations is possible to produce real roots.
    Also tests on solving for quadratic equations.
    """

    def __init__(self, seed_value=None, discriminant_upper_limit=20):
        super().__init__(seed_value=seed_value)
        self.discriminant_upper_limit = discriminant_upper_limit

    def calculations(self):
        # Generate the three discriminants. `discriminant1` will form the equation with real roots.
        discriminant1 = self.random.randint(1, self.discriminant_upper_limit) ** 2
        discriminant2 = -self.random.randint(1, self.discriminant_upper_limit) ** 2
        discriminant3 = -self.random.randint(1, self.discriminant_upper_limit) ** 2

        # Generate the three questions
        q1, coefficients = self.generate_equations(discriminant1, return_coefficients=True)
        q2 = self.generate_equations(discriminant2)
        q3 = self.generate_equations(discriminant3)

        # Shuffle the questions
        questions = [q1, q2, q3]
        self.random.shuffle(questions)
        self.question = questions

        # Calculate the roots for the "correct" equation
        roots = self.quadratic_formula(coefficients[0], coefficients[1], coefficients[2])
        self.answer = roots

    def generate_question(self):
        string = "Solve the quadratic equation with real roots (Equation \\eqref{q12:eqn1}, Equation " \
                 "\\eqref{q12:eqn2} or Equation \\eqref{q12:eqn3}) for $x$:"

        for i, q in enumerate(self.question):
            string += f"$$\\begin{{equation}}{q}\\label{{q12:eqn{i + 1}}}\\end{{equation}}$$"

        return string

    def generate_answer(self):
        return [mathematical_round(min(self.answer), 3), mathematical_round(max(self.answer), 3)]

    def generate_input_fields_prefixes(self):
        return ["$x_1=$", "$x_2=$"]

    def get_coefficients(self, discriminant):
        # Generate a value for `b`
        possible_b = list(range(1, self.discriminant_upper_limit))

        try:
            possible_b.remove(int(math.sqrt(discriminant)))  # We don't want a case where a*c = 0
        except ValueError:
            pass

        b = self.random.choice(possible_b)

        # Calculate the value of the product of `a` and `c`
        ac = (b ** 2 - discriminant) / 4

        # Generate the values of `a` and `c`
        if ac == int(ac):  # ac is an integer
            # Get a possible factor set of `ac`
            factors = self.get_factors(ac)
            factor_set = self.random.choice(factors)  # Choose one set of factors

            # Decide which factor is `a` and which factor is `c`
            a_c = self.random.sample([0, 1], k=2)  # First index is a, second index is c
            a = factor_set[a_c[0]]
            c = factor_set[a_c[1]]

        else:  # ac is a float
            # Express the float as a fraction
            integer_ratio = ac.as_integer_ratio()

            # Get factors of each of the parts of the `integer_ratio`
            numerator_factors = self.get_factors(integer_ratio[0])
            denominator_factors = self.get_factors(integer_ratio[1])

            # Get all combinations of the factors
            all_combinations = []
            numerator_permutations = itertools.permutations(numerator_factors, len(denominator_factors))

            for each_permutation in numerator_permutations:
                zipped = zip(each_permutation, denominator_factors)
                all_combinations.append(list(zipped))

            combinations = []
            for elem in all_combinations:
                for e in elem:
                    combinations.append(e)

            combinations = list(set(combinations))

            # Choose one combination
            combination = self.random.choice(combinations)

            # Get which indices a and c should take from the combination
            a_indices = self.random.sample([0, 0, 1, 1], k=2)
            c_indices = [int(not a_indices[0]), int(not a_indices[1])]

            # Get the values
            a = Fraction(combination[0][a_indices[0]], combination[1][a_indices[1]])
            c = Fraction(combination[0][c_indices[0]], combination[1][c_indices[1]])

        return a, b, c

    def generate_equations(self, discriminant, return_coefficients=False):
        # Generate the coefficients
        while True:
            try:
                a, b, c = self.get_coefficients(discriminant)
                break
            except IndexError:
                pass

        # Generate the question
        q = f"\t{a} * x**2 {'-' if b < 0 else '+'} {abs(b)} * x {'-' if c < 0 else '+'} {abs(c)}"
        q = latex(parse_expr(q)) + " = 0"

        # Return the values
        if not return_coefficients:
            return q
        else:
            return q, (a, b, c)

    @staticmethod
    def get_factors(n):
        # Create an empty list for factors
        factors = []

        if n > 0:
            # Loop over all factors
            for i in range(1, int(n ** 0.5) + 1):
                if n % i == 0:
                    factors.append((i, int(n // i)))
        elif n < 0:
            k = -n
            # Loop over all factors
            for i in range(1, int(k ** 0.5) + 1):
                if k % i == 0:
                    factors.append((i, int(n // i)))
                    factors.append((-i, int(k // i)))  # The product must be a negative number
        else:
            factors = [(0, 0)]

        # Return the list of factors
        return factors

    @staticmethod
    def quadratic_formula(a, b, c):
        p = -b
        q = math.sqrt(b ** 2 - (4 * a * c))
        r = 1 / (2 * a)

        return (p + q) * r, (p - q) * r


# DEBUG CODE
if __name__ == "__main__":
    question = Q6(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
