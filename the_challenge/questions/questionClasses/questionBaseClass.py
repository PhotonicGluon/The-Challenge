"""
questionBaseClass.py

Created on 2020-08-21
Updated on 2020-09-11

Copyright Ryan Kan 2020

Description: The base class of all other questions.
"""

# IMPORTS
from random import Random


# CLASSES
class Question:
    """
    The overarching Question class. Used to defined all the other questions.
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
        return None

    def generate_question(self):
        """
        This method returns the question stem of the question.

        Returns:
            str: Question stem.
        """

        # This method is to be overwritten by the questions themselves.
        return None

    def generate_answer(self):
        """
        This method returns the answer of the question.
        - Note that an answer in a LIST with square brackets [ ] means that all permutations of the sub-answers in the
          list will be accepted as answers.
        - Note that an answer in a TUPLE with rounded brackets ( ) means that it is the ONLY accepted answer.


        Returns:
            Union[int, float, str, List[Union[int, float]], Tuple[Union[int, float]]]: Answer.
        """

        # This method is to be overwritten by the questions themselves.
        return None

    def answer_input_fields_prefix(self):
        """
        This method returns the prefixes to all the input fields for answers.

        Returns:
            List[str]: List of prefix(es).
        """

        # This method is to be overwritten by the questions themselves.
        return None
