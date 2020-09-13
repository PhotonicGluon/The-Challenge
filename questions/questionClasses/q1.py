"""
q1.py

Created on 2020-08-21
Updated on 2020-09-10

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
from questions.questionClasses import Question


# CLASSES
class Q1(Question):
    """
    Q1:
    Just simple adding/subtracting.
    """

    def calculations(self):
        # CONSTANTS
        operators = ["+", "-", "*", "/"]

        # CALCULATIONS
        a = self.random.randint(1, 20)
        b = self.random.randint(1, 20)

        self.question = f"{a} {self.random.choice(operators)} {b}"
        self.answer = round(eval(self.question), 3)

    def generate_question(self):
        string = f"State the value of:$${self.question.replace('*', chr(92) + 'times').replace('/', chr(92) + 'div')}$$"  # Note: chr(92) = "\"
        return string

    def generate_answer(self):
        return self.answer

    def answer_input_fields_prefix(self):
        return ["Answer:"]


# DEBUG CODE
if __name__ == "__main__":
    question = Q1(seed_value=1123581321)
    question.calculations()
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
