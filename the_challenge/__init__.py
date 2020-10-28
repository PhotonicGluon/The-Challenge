"""
__init__.py

Created on 2020-09-19
Updated on 2020-10-28

Copyright Ryan Kan 2020

Description: This file contains the main Flask application for The Challenge.
"""

# IMPORTS
import os
import uuid

import simplejson as json
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, flash, make_response, abort
from flask_session import Session

from the_challenge.misc import verify_otp, check_internet_connection
from the_challenge.questions import QuestionHandler, process_user_answer, check_user_answer
from the_challenge.version import __version__

# FLASK SETUP
# Define basic things
app = Flask(__name__)
app.config.from_pyfile("baseConfig.py")

# Setup session `sess`
sess = Session()

# CONSTANTS
SUCCESS_TIMES_FILE = os.path.join(app.instance_path, "Success_Times.json")

# PRE-SERVER STARTING CODE
# Ensure that the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Ensure that the `SUCCESS_TIMES_FILE` exist
if not os.path.isfile(SUCCESS_TIMES_FILE):
    # Create the file
    with open(SUCCESS_TIMES_FILE, "w+") as tempFile:
        json.dump({}, tempFile)
        tempFile.close()

# FLASK SETUP (CONTINUED)
# Get the instance's `config.py` file
try:
    app.config.from_pyfile(os.path.join(app.instance_path, "config.py"))
except OSError:
    print("The instance's `config.py` file was not found. Using default settings. (INSECURE!)")

# Initialise plugins
sess.init_app(app)


# FUNCTIONS
def clear_user_data():
    if "quiz_starting" in session:
        session.pop("quiz_starting")

    if "starting_challenge" in session:
        session.pop("starting_challenge")

    if "challenge_won" in session:
        session.pop("challenge_won")


# WEBSITE'S PAGES
# 'Functional' Pages
@app.route("/secret/check-connection", methods=["GET"])
def check_connection():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if verify_otp(key, "INTERNET2CONNECT"):
        # Check if the user can access the example domain by IANA
        if check_internet_connection():
            return "y0u-4r3-c0nn3c73d!"
        else:
            return "y0u-4r3-n07-c0nn3c73d"
    else:
        return abort(403)


@app.route("/secret/start-challenge", methods=["GET"])
def start_challenge():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if verify_otp(key, "START2CHALLENGE3"):
        # Clear data
        clear_user_data()

        # Start the quiz
        session["quiz_starting"] = True
        return url_for("load_challenge")  # Load the url into the javascript script
    else:
        return abort(403)


@app.route("/secret/setup-questions", methods=["GET"])
def setup_questions():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if verify_otp(key, "SETUP2QUESTIONS3"):
        # Setup question bank
        question_handler = QuestionHandler()

        # Setup the questions
        generated_questions, input_field_prefixes, answers = question_handler.setup_questions()

        # Get the image from Q4
        q4_image_data = generated_questions[3][1]

        # Fix that entry to be only the question string
        generated_questions[3] = generated_questions[3][0]

        # Save `generated_questions` and `input_field_prefixes` to the session
        run_data = {"questions": generated_questions, "prefixes": input_field_prefixes}

        session["RunData"] = json.dumps(run_data)
        session["Q4_Image"] = q4_image_data  # Has to be handled separately due to its large size

        # Return the json object
        return jsonify(questions=generated_questions)

    else:
        return abort(403)


@app.route("/secret/redirect-to-the-challenge", methods=["GET"])
def redirect_to_the_challenge():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if verify_otp(key, "REDIRECTING2TO3THE4CHALLENGE5NOW"):
        session["starting_challenge"] = True
        return url_for("the_challenge")

    else:
        return abort(403)


@app.route("/secret/check-answer", methods=["GET"])
def check_answer():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)
    question_no = request.args.get("question_no", None, type=int)
    user_answer = request.args.getlist("user_answer[]")  # Gets all the elements that has this tag and puts it in a list

    # Check the key
    if verify_otp(key, "I2WANT3TO4CHECK5MY6ANSWER7CAN2YOU3CHECK4"):
        # Get the correct answer
        answer = json.loads(session["RunData"])["answers"][question_no - 1]

        # Process the user's answer
        processed_user_answer = process_user_answer(user_answer)

        # Check user's answer
        correct = check_user_answer(processed_user_answer, answer)

        return jsonify(correct=correct)
    else:
        return abort(403)


@app.route("/secret/success-handler", methods=["GET"])
def success_handler():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)
    user_id = request.args.get("user_id", None, type=str)
    time_remaining = request.args.get("time_remaining", None, type=float)

    # Check the key
    if verify_otp(key, "CONGRATULATIONS2YOU3COMPLETED4THE5CHALLENGE6YAY7"):
        # Save the time remaining to the JSON file
        with open(SUCCESS_TIMES_FILE, "r") as infile:
            if len(infile.read()) > 5:
                infile.seek(0)  # Move file pointer to the front of the file
                success_times = json.load(infile)
            else:
                success_times = {}
            infile.close()

        # Try to get an existing time
        try:
            existing_time = success_times[user_id]

        except KeyError:
            existing_time = 0

        # Round the obtained time
        new_time = round(time_remaining, 4)

        # Get the best time
        best_time = max(new_time, existing_time)

        # If the new time is not the best time show a popup
        if best_time != new_time:
            flash(f"The time left for this attempt is {new_time} seconds, which unfortunately did not beat your best "
                  f"time.")

        # Save the best time to the success times' dictionary
        success_times[user_id] = best_time

        # Write the updated dictionary to the file
        with open(SUCCESS_TIMES_FILE, "w") as outfile:
            json.dump(success_times, outfile)
            outfile.close()

        # Return the success page
        return url_for("success", userid=user_id)

    else:
        return abort(403)


@app.route("/secret/failure", methods=["GET"])
def failure():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if key == "0h-n0-y0u-f41l3d":
        flash("You ran out of time! Try again.")
        return url_for("main_page")

    else:
        return abort(403)


# Hidden Pages
@app.route("/load-challenge")
def load_challenge():
    if "quiz_starting" in session and session["quiz_starting"]:
        session["quiz_starting"] = False  # Reset the flag
        return render_template("the_challenge/loading.html")
    else:
        if "quiz_starting" in session:
            flash("Please do not reload the page when playing The Challenge.")

        clear_user_data()
        return redirect(url_for("main_page"))


@app.route("/the-challenge")
def the_challenge():
    if "starting_challenge" in session and session["starting_challenge"]:
        session["starting_challenge"] = False  # Reset the flag
        return render_template("the_challenge/questions.html")
    else:
        if "starting_challenge" in session:
            flash("Please do not reload the page when playing The Challenge.")

        clear_user_data()
        return redirect(url_for("main_page"))


@app.route("/success/<userid>")
def success(userid):
    # Get the time left from the JSON file
    with open(SUCCESS_TIMES_FILE, "r") as f:
        success_times = json.load(f)
        f.close()

    # Try to get the success time
    try:
        success_time = success_times[userid]
    except KeyError:
        # Raise a 404 error
        return abort(404)

    # Render the template
    return render_template("the_challenge/success.html", uuid=userid, time=success_time)


# Root Pages
@app.route("/")
def main_page():
    response = make_response(render_template("index/mainPage.html", version=__version__))
    if not request.cookies.get("ChallengeUUID"):
        # Generate a unique UUID for the user and set it in a cookie
        response.set_cookie("ChallengeUUID", str(uuid.uuid4()), max_age=60 * 60 * 24 * 365 * 10)

    if "quiz_starting" in session:
        clear_user_data()

    return response


@app.route("/licenses")
def licenses():
    return render_template("index/licenses.html")


@app.route("/try-out-algebra-input")
def algebra_input():
    return render_template("index/algebraInput.html")


# Error pages
@app.errorhandler(403)
def forbidden(e):
    _ = e  # Remove the error details from memory
    return render_template("base/403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    _ = e  # Remove the error details from memory
    return render_template("base/404.html"), 404


# APP FACTORY FUNCTION
def init_app():
    print("Starting server.")
    app.run()


if __name__ == "__main__":
    init_app()
