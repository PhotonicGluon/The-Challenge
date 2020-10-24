"""
q3.py

Created on 2020-08-21
Updated on 2020-10-24

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from the_challenge.misc import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q3(Question):
    """
    Q3:
    Simple "solving for x" problem. x is in a linear equation and the solution is trivial.
    """

    def calculations(self):
        # CONSTANTS
        operators = ["+", "-"]

        # CALCULATIONS
        a = self.random.randint(10, 99)
        b = self.random.randint(100, 999)
        c = self.random.randint(100, 999)

        s = self.random.choice(operators)  # Choose a sign

        self.question = f"{a} x {s} {b} = {c}"
        self.answer = mathematical_round((-eval(f"{s}{b}") + c) / a, 3)

    def generate_question(self):
        string = f"Solve for the value of $x$ in the equation $${self.question}$$"
        return string

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["$x=$"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q3(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
