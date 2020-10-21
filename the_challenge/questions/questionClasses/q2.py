"""
q2.py

Created on 2020-08-21
Updated on 2020-10-21

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from the_challenge.misc import mathematical_round
from the_challenge.questions.questionClasses.questionBaseClass import Question


# CLASSES
class Q2(Question):
    """
    Q2:
    Harder addition/subtraction/multiplication/division question.
    """

    def calculations(self):
        # CONSTANTS
        operators = ["+", "-", "*", "/"]

        # CALCULATIONS
        a = self.random.randint(100, 999)
        b = self.random.randint(100, 999)
        c = self.random.randint(100, 999)

        chosen_operators = self.random.sample(operators, k=2)

        self.question = f"{a} {chosen_operators[0]} {b} {chosen_operators[1]} {c}"
        self.answer = mathematical_round(eval(self.question), 3)

    def generate_question(self):
        treated_expr = self.question.replace("*", "\\times").replace("/", "\\div")
        string = f"State the value of:$${treated_expr}$$"

        return string

    def generate_answer(self):
        return self.answer

    def generate_input_fields_prefixes(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q2(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
