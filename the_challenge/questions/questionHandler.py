"""
questionHandler.py

Created on 2020-08-26
Updated on 2020-10-23

Copyright Ryan Kan 2020

Description: A class which handles the functions of all the questions.
"""

# IMPORTS
from random import seed

from the_challenge.questions import *


# CLASSES
class QuestionHandler:
    def __init__(self, seed_value=None):
        """
        Initialise the question handler.

        Args:
            seed_value (Union[str, None]):  The value to initialise the randomiser to.
        """

        # Set the randomiser to the seed
        seed(seed_value)

        # Define the list of question classes
        self.question_classes = [
            Q1(seed_value),
            Q2(seed_value),
            Q3(seed_value),
            Q4(seed_value),
            Q5(seed_value),
            Q6(seed_value),
            Q7(seed_value),
            Q8(seed_value),
            Q9(seed_value),
            Q10(seed_value),
            Q11(seed_value),
            Q12(seed_value),
            Q13(seed_value),
            Q14(seed_value),
        ]

        self.questions = []  # Where all the question stems will be stored
        self.input_field_prefixes = []  # Where all the answers' input fields' prefixes will be stored
        self.answers = []  # Where all the answers will be stored

    def setup_questions(self):
        """
        Sets up the questions in The Challenge.

        Returns:
            List[str]:  A list of stings, which are the questions.

            List[str]:  A list of strings, which are the prefixes to all the input fields.

            List[Union[str, int, float, List[Union[int, float]]]]:  A list of answers.
        """

        # Perform calculations for all questions
        for question_class in self.question_classes:
            # Run the calculations function
            question_class.calculations()

            # Generate the questions
            self.questions.append(question_class.generate_question())

            # Generate all the input fields' prefixes
            self.input_field_prefixes.append(question_class.generate_input_fields_prefixes())

            # Generate the answers
            self.answers.append(question_class.generate_answer())

        return self.questions, self.input_field_prefixes, self.answers


# DEBUG CODE
if __name__ == "__main__":
    questionHandler = QuestionHandler(seed_value="Theorem")
    questions, prefixes, answers = questionHandler.setup_questions()
