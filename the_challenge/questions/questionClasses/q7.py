"""
q7.py

Created on 2020-08-21
Updated on 2020-10-30

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from sympy import latex, binomial
from sympy.parsing.sympy_parser import parse_expr

from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q7(Question):
    """
    Q7:
    Determine the r-th term of a binomial expansion.
    """

    def calculations(self):
        # Generate the binomial expression
        a = self.random.randint(1, 9)
        b = self.random.randint(1, 3)
        c = self.random.randint(1, 9)
        d = self.random.randint(1, 9)
        e = self.random.randint(1, 3)
        f = self.random.randint(4, 8)

        sign = self.random.choice(["+", "-"])

        binomial_expression = latex(parse_expr(f"({a} * x ** {b} {sign} {c} / ({d} * x ** {e})) ** {f}"))

        # Generate the term which the user is supposed to calculate
        r = self.random.randint(2, f - 1)

        # Generate that term
        rth_term = f"{binomial(f, r - 1)} * (({a} * x ** {b}) ** {f - r + 1}) * (({sign} {c} / ({d} * x ** {e})) " \
                   f"** {r - 1})"
        rth_term = latex(parse_expr(rth_term))

        # Save variables to `self.question` and `self.answer`
        self.question = [r, binomial_expression]
        self.answer = rth_term

    def generate_question(self):
        string = f"Determine the {self.ordinal(self.question[0])} term in the binomial expansion of " \
                 f"$${self.question[1]}$$"
        return string

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["Answer:"]

    @staticmethod
    def ordinal(n):
        n = int(n)
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]

        if 11 <= n % 100 <= 13:
            suffix = "th"

        return f"{n}<sup>{suffix}</sup>"


# DEBUG CODE
if __name__ == "__main__":
    question = Q7(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
