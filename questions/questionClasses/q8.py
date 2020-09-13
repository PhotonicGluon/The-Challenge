"""
q8.py

Created on 2020-08-21
Updated on 2020-09-10

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
import numpy as np
from matplotlib import pyplot as plt

from questions.questionClasses import Question


# CLASSES
class Q8(Question):
    """
    Q8:
    Determine values of a, b and c in the expression `y = a * sin(x/b) + c` or `y = a * cos(x/b) + c` when given a
    graph of that function.
    """

    def __init__(self, seed_value=None, figure_file_path="Q8.png"):
        super().__init__(seed_value=seed_value)
        self.figure_file_path = figure_file_path

    def calculations(self):
        # Generate values for a, b and c
        a = self.random.choice([self.random.randint(-5, -1), self.random.randint(1, 5)])
        b = self.random.randint(1, 4)
        c = self.random.randint(-10, 10)

        # Choose a function to plot
        sin_or_cos = self.random.choice([np.sin, np.cos])

        # Generate the domain
        x = np.arange(0, 360 * b, 0.5)

        # Generate the function
        func = a * sin_or_cos(self.deg2rad(x) / b) + c

        # Set gridlines for both axes
        x_ticks = np.arange(0, 360 * b + 1, 360 * b / 4)
        y_ticks = np.arange(-abs(a) + c, abs(a) + c + 1, abs(a))

        # Create a figure and an axis
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        # Set ticks on the plot
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)

        # Or if you want different settings for the grids:
        ax.grid(which="minor", alpha=0.1)
        ax.grid(which="major")

        # Label the axes
        ax.set_xlabel("x°")

        if sin_or_cos == np.sin:
            eqn = r"y = a \sin\left(\frac{x}{b}\right) + c"
            ax.set_ylabel(r"y")
        else:
            eqn = r"y = a \cos\left(\frac{x}{b}\right) + c"
            ax.set_ylabel(r"y")

        # Plot the function
        ax.plot(x, func)

        # Save the plot to a temporary file
        plt.savefig(self.figure_file_path, bbox_inches="tight")
        plt.close()

        # Set values for `self.question` and `self.answer`
        self.question = [eqn, self.figure_file_path]
        self.answer = (a, b, c)

    def generate_question(self, show_graph=False):
        # Generate the question
        string = f"Determine the values of $a$, $b$ and $c$ in $${self.question[0]}$$ given the graph of that " \
                 f"equation as shown above."

        # Show the graph (if allowed)
        if show_graph:
            from PIL import Image
            img = Image.open(self.question[1])
            plt.imshow(img)
            plt.axis("off")
            plt.show()

        return string

    def generate_answer(self):
        return self.answer

    def answer_input_fields_prefix(self):
        return ["$a=$", "$b=$", "$c=$"]

    @staticmethod
    def deg2rad(deg):
        return deg * np.pi / 180


# DEBUG CODE
if __name__ == "__main__":
    question = Q8(seed_value=1123581321)
    question.calculations()
    print(question.generate_question(show_graph=True))
    print("[ANSWER]", question.generate_answer())
