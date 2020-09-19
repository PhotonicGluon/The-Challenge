# IMPORTS
import os
import time
import uuid
from multiprocessing import Process, Value

import simplejson as json
from flask import Flask, request, redirect, url_for, render_template, session, jsonify, flash, make_response
from flask_socketio import SocketIO

from questions import QuestionBank, process_user_answer, check_user_answer

# FLASK SETUP
app = Flask(__name__)
app.secret_key = b"1123581321345589144"
socketIO = SocketIO(app)

# CONSTANTS
IMAGE_DELETION_TIME_FILE = "JSON_Files/Image_Deletion_Time.json"  # This will store all the image deletion times
SUCCESS_TIMES_FILE = "JSON_Files/Success_Times.json"  # This will store all the success times


# FUNCTIONS
def clear_user_data():
    if request.cookies.get("ChallengeUUID"):
        try:
            os.remove(f"static/others/q8/Q8_{request.cookies.get('ChallengeUUID')}.png")  # Remove this image
        except FileNotFoundError:
            pass

    if "quiz_starting" in session:
        session.pop("quiz_starting")

    if "starting_challenge" in session:
        session.pop("starting_challenge")

    if "challenge_won" in session:
        session.pop("challenge_won")


def check_image_deletion_time(loop_on):
    while True:
        if loop_on:
            print("Image Deletion Check")

            # Open the JSON file to get all the image deletion times
            with open(IMAGE_DELETION_TIME_FILE, "r") as f:
                image_deletion_time = json.load(f)
                f.close()

            # Extract all IDs which are in that file
            deleted_ids = []
            for unique_id in image_deletion_time:
                due_to_delete = image_deletion_time[unique_id] - time.time()

                if due_to_delete < 0:  # It is already due to delete
                    try:
                        # Remove the image
                        os.remove(f"static/others/q8/Q8_{unique_id}.png")  # Remove the image
                        print(f"\t- Deleted `{unique_id}`'s Q8 image (timeout)")

                        # Add that id to the list of `deleted_ids`
                        deleted_ids.append(unique_id)
                    except FileNotFoundError:
                        pass

            # Delete all entries which has a UUID that is in `deleted_ids`
            for uid in deleted_ids:
                image_deletion_time.pop(uid)

            # Update the JSON file
            with open(IMAGE_DELETION_TIME_FILE, "w") as outfile:
                json.dump(image_deletion_time, outfile)
                outfile.close()

        time.sleep(60)  # Check again after 60 seconds


# PAGES
# 'Functional' Pages
@app.route("/secret/check_connection")
def check_connection():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if key == "connection":
        # Since the user is able to access this page they are online
        return "Connected"
    else:
        # Redirect back to index
        return redirect(url_for("index"))


@app.route("/secret/start_challenge")
def start_challenge():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if key == "".join([chr(950 + x) for x in [2 * 3, 3 * 5, 13, 2 * 7, 3, 2 ** 2, 2 * 11]]):
        # Clear data
        clear_user_data()

        # Start the quiz
        session["quiz_starting"] = True
        return url_for("load_challenge")  # Load the url into the javascript script
    else:
        return redirect(url_for("index"))


@app.route("/secret/setup_questions")
def setup_questions():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if key == "".join(chr(x) for x in [6 ** 2, 2 ** 2 * 3 * 17 * 41, 2 ** 2 * 241, 3 ** 2 * 13, 17 ** 2 * 29]):
        # Setup question bank
        question_bank = QuestionBank(q8_file_path=f"static/others/q8/Q8_{request.cookies.get('ChallengeUUID')}.png")

        # Setup the questions
        questions, input_field_prefixes, answers = question_bank.setup_questions()

        # Save `questions` and `answers` to the session
        run_data = {"questions": questions, "prefixes": input_field_prefixes, "answers": answers}
        session["RunData"] = json.dumps(run_data)

        # Return the json object
        return jsonify(questions=questions)

    else:
        return redirect(url_for("index"))


@app.route("/secret/redirect-to-the-challenge")
def redirect_to_the_challenge():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if key == "".join([chr(158 ** 2 + 36 + x) for x in [19 ** 2, 11 ** 2 - 9][::-1]][::-1]):
        session["starting_challenge"] = True
        return url_for("the_challenge")

    else:
        return redirect(url_for("index"))


@app.route("/secret/check-answer")
def check_answer():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)
    question_no = request.args.get("question_no", None, type=int)
    user_answer = request.args.getlist("user_answer[]")  # Gets all the elements that has this tag and puts it in a list

    # Check the key
    if key == "CHECK":
        # Get the correct answer
        answer = json.loads(session["RunData"])["answers"][question_no - 1]

        # Process the user's answer
        processed_user_answer = process_user_answer(user_answer)

        # Check user's answer
        correct = check_user_answer(processed_user_answer, answer)

        return jsonify(correct=correct)
    else:
        return redirect(url_for("index"))


@app.route("/secret/success-handler")
def success_handler():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)
    user_id = request.args.get("user_id", None, type=str)
    time_remaining = request.args.get("time_remaining", None, type=float)

    # Check the key
    if key == "a-winner-is-you":
        # Save the time remaining to the JSON file
        with open(SUCCESS_TIMES_FILE, "r") as infile:
            if len(infile.read()) <= 5:
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

        # Save the best time to the dictionary
        success_times[user_id] = round(max(time_remaining, existing_time), 4)

        # Write the updated dictionary to the file
        with open(SUCCESS_TIMES_FILE, "w") as outfile:
            json.dump(success_times, outfile)
            outfile.close()

        # Return the success page
        return url_for("success_specific", userid=user_id)

    else:
        return redirect(url_for("index"))


@app.route("/secret/failure")
def failure():
    # Get the page's arguments
    key = request.args.get("key", None, type=str)

    # Check the key
    if key == "fail":
        flash("You ran out of time! Try again.")
        return url_for("index")

    else:
        return redirect(url_for("index"))


# Hidden Pages
@app.route("/load_challenge")
def load_challenge():
    if "quiz_starting" in session and session["quiz_starting"]:
        session["quiz_starting"] = False  # Reset the flag
        return render_template("the_challenge/loading.html")
    else:
        if "quiz_starting" in session:
            flash("Please do not reload the page when playing The Challenge.")

        clear_user_data()
        return redirect(url_for("index"))


@app.route("/the-challenge")
def the_challenge():
    if "starting_challenge" in session and session["starting_challenge"]:
        session["starting_challenge"] = False  # Reset the flag
        return render_template("the_challenge/questions.html")
    else:
        if "starting_challenge" in session:
            flash("Please do not reload the page when playing The Challenge.")

        clear_user_data()
        return redirect(url_for("index"))


@app.route("/success/<userid>")
def success_specific(userid):
    # Get the time left from the JSON file
    with open(SUCCESS_TIMES_FILE, "r") as f:
        success_times = json.load(f)
        f.close()

    # Try to get the success time
    try:
        success_time = success_times[userid]
    except KeyError:
        flash("The desired user's info cannot be found.")
        return redirect(url_for("index"))

    # Render the template
    return render_template("the_challenge/success.html", uuid=userid, time=success_time)


# SocketIO Pages
@socketIO.on("Heartbeat")
def heartbeat(heartbeat_data):
    # Check if the `heartbeat_data` has info in it
    if len(list(heartbeat_data)) != 0:
        # Get the UUID
        uuid_received = heartbeat_data["uuid"]
        # print(f"Heartbeat data received: {uuid_received}")

        # Extend the time to delete the image file
        with open(IMAGE_DELETION_TIME_FILE, "r") as infile:
            if len(infile.read()) <= 5:
                infile.seek(0)  # Move file pointer to the front of the file
                image_deletion_time = json.load(infile)
            else:
                image_deletion_time = {}
            infile.close()

        image_deletion_time[uuid_received] = time.time() + 60 * 5  # Extend the time by 5 minutes

        with open(IMAGE_DELETION_TIME_FILE, "w") as outfile:
            json.dump(image_deletion_time, outfile)
            outfile.close()
    else:
        print("A user tried to send a heartbeat but their cookies were disabled.")


# Root Pages
@app.route("/")
def index():
    response = make_response(render_template("index/index.html"))
    if not request.cookies.get("ChallengeUUID"):
        # Generate a unique UUID for the user and set it in a cookie
        response.set_cookie("ChallengeUUID", str(uuid.uuid4()), max_age=60 * 60 * 24 * 365 * 10)

    if "quiz_starting" in session:
        clear_user_data()

    return response


@app.route("/licenses")
def licenses():
    return render_template("index/licenses.html")


# Error pages
@app.errorhandler(404)
def page_not_found(e):
    # Note that we set the 404 status explicitly
    _ = e
    return render_template("base/404.html"), 404


if __name__ == "__main__":
    print("Starting server.")
    # Define the image deletion checker function
    image_deletion_checker_on = Value("b", True)
    image_deletion_checker = Process(target=check_image_deletion_time, args=(image_deletion_checker_on,))

    # Start checking for deletable images
    image_deletion_checker.start()

    # Run the app
    socketIO.run(app)

    # Join all processes
    image_deletion_checker.join()
