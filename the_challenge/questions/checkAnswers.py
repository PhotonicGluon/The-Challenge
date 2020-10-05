"""
checkAnswers.py

Created on 2020-09-11
Updated on 2020-10-04

Copyright Ryan Kan 2020

Description: Contains all functions to process and check the users' answers
"""

# IMPORTS
from itertools import permutations

from sympy.parsing.latex import parse_latex


# FUNCTIONS
def handle_latex_preprocessing(latex_string):
    """
    Preprocesses the LaTeX string to be parsed in Sympy.

    Args:
        latex_string (str): The string with the LaTeX input.

    Returns:
        str: The cleaned LaTeX string.
    """

    # Remove any unneeded tags
    try:
        latex_string = latex_string.replace(" ", "").replace("\left", "").replace("\\right", "").replace("\\,", "")
    except AttributeError:
        pass

    # Return the processes latex string
    return latex_string


def process_user_answer(user_answer):
    """
    This method preprocesses the user's answer for checking.

    Args:
        user_answer (List[str]): The unprocessed answer.

    Returns:
        Union[str, int, float, List[Union[int, float]], Tuple[Union[int, float]]]: The processed answer
    """

    processed_answer = []
    for x in user_answer:
        # Check if the string can be expressed as a integer
        try:
            processed_answer.append(int(x))
        except ValueError:
            # Check if the string can be expressed as a float
            try:
                processed_answer.append(float(x))
            except ValueError:
                processed_answer.append(handle_latex_preprocessing(x))

    if len(processed_answer) == 1:
        return processed_answer[0]
    else:
        return processed_answer


def check_user_answer(user_answer, calculated_answer):
    """
    This method checks the user's answer with the calculated answer.

    Args:
        user_answer (Union[str, int, float, List[Union[int, float]]], Tuple[Union[int, float]]])
        calculated_answer (Union[str, int, float, List[Union[int, float]], Tuple[Union[int, float]]]])

    Returns:
        bool: Returns True then the user's answer is correct. If it is wrong it will return False instead.
    """

    # COMPUTATION
    # Output the correct answer
    print("Correct answer:", calculated_answer)

    # Determine the type of the calculated answer
    if isinstance(calculated_answer, tuple):
        # Check if the user's answers is equal to the calculated answers
        if user_answer == calculated_answer:
            return True
        else:
            return False

    elif isinstance(calculated_answer, list):
        # Check if the user's answer is equal to one of the permutations of the list
        all_permutations = [list(x) for x in list(permutations(calculated_answer))]
        for permutation in all_permutations:
            if user_answer == permutation:
                return True
        return False

    elif isinstance(calculated_answer, int) or isinstance(calculated_answer, float):
        # For debugging purposes, output the calculated answer
        print("Correct answer:", calculated_answer)

        # Check if the user's answer is equal to the calculated answer
        if user_answer == calculated_answer:
            return True
        else:
            return False

    else:  # Strings
        # Parse the correct answer's LaTeX data
        calculated_answer = parse_latex(handle_latex_preprocessing(calculated_answer))

        # Parse the user's LaTeX input
        parsed_user_answer = parse_latex(str(handle_latex_preprocessing(user_answer)))  # Cast to string just in case

        # Compare the two answers
        if parsed_user_answer.equals(calculated_answer):
            return True
        else:
            return False


# DEBUG CODE
if __name__ == "__main__":
    # Test the processing
    integer = process_user_answer(["6"])
    float1 = process_user_answer(["12.3"])
    float2 = process_user_answer(["12.34"])
    float3 = process_user_answer(["12.345"])
    integerList = process_user_answer(["1", "2", "3"])
    floatList = process_user_answer(["1.2", "2.34", "3.456"])
    stringList = process_user_answer(["sin(x)"])

    # Print the answers
    print(integer, type(integer))
    print(float1, type(float1))
    print(float2, type(float2))
    print(float3, type(float3))
    print(integerList)
    print(floatList)
    print(stringList)