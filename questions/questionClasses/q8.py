"""
q8.py

Created on 2020-08-21
Updated on 2020-09-19

Copyright Ryan Kan 2020

Description: A file which holds the designated question class.
"""

# IMPORTS
import numpy as np
import plotly.graph_objects as go

from questions.questionClasses.questionBaseClass import Question


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
        x = np.arange(0, 360 * b + 0.5, 0.5)  # Add 0.5 to make the final point be 360 * b

        # Generate the function
        func = a * sin_or_cos(self.deg2rad(x) / b) + c

        # Create a layout and a figure
        layout = go.Layout(autosize=True, margin={"l": 20, "r": 20, "t": 20, "b": 20})
        fig = go.Figure(layout=layout)

        # Update theme
        fig.update_layout(template="plotly_white")  # Make it bend in with the webpage

        # Setup the axes
        fig.update_xaxes(title_text="$x^\\circ$", tick0=0, dtick=360 * b / 4)
        fig.update_yaxes(title_text="$y$", tick0=-a + c, dtick=abs(a))

        # Plot the function
        fig.add_trace(go.Scatter(x=x, y=func))

        # Save the plot to an image file
        fig.write_image(self.figure_file_path, width=600, height=350, scale=2)

        # Choose the correct equation to display for the question
        if sin_or_cos == np.sin:
            eqn = r"y = a \sin\left(\frac{x}{b}\right) + c"
        else:
            eqn = r"y = a \cos\left(\frac{x}{b}\right) + c"

        # Set values for `self.question` and `self.answer`
        self.question = [eqn, self.figure_file_path]
        self.answer = (a, b, c)

    def generate_question(self, show_graph=False):
        string = f"Determine the values of $a$, $b$ and $c$ in $${self.question[0]}$$ given the graph of that " \
                 f"equation as shown above."

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
    print(question.generate_question())
    print("[ANSWER]", question.generate_answer())
