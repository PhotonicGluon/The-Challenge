"""
questionBaseClass.py

Created on 2020-08-21
Updated on 2020-10-30

Copyright Ryan Kan 2020

Description: The base class of all other questions.
"""

# IMPORTS
from random import Random


# CLASSES
class Question:
    """
    The overarching Question class. Used to define all the other questions.
    """

    def __init__(self, seed_value=None):
        # Instantiate properties
        self.question = None  # This will store the finished question string
        self.answer = None  # This will store the answer

        self.random = Random()  # This is the random generator

        # Set the seed of the random generator
        self.random.seed(seed_value)

    def calculations(self):
        """
        This method does all the calculations for the question.
        """

        # This method is to be overwritten by the questions themselves.
        pass

    def generate_question(self):
        """
        This method returns the question stem of the question.

        Returns:
            str:    The question stem.
        """

        # This method is to be overwritten by the questions themselves.
        return None

    def generate_answer(self):
        """
        This method returns the answer of the question.
        -   Note that an answer in a LIST with square brackets [ ] means that all permutations of the sub-answers in the
            list will be accepted as answers.

        Returns:
            Union[int, float, str, List[Union[int, float]]]:    The generated answer.
        """

        # This method is to be overwritten by the questions themselves.
        return None

    def generate_input_fields_prefixes(self):
        """
        This method returns the prefixes to all the input fields for answers.

        Returns:
            List[str]:  List of prefixes for the input fields.
        """

        # This method is to be overwritten by the questions themselves.
        return None
