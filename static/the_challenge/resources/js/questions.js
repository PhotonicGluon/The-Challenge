const DURATION_OF_THE_CHALLENGE = 900;  // In seconds

$(document).ready(async () => {
    // Get DOM objects
    const questionContainer = $("#question-container")[0];  // Get the individual `div` element, not the jQuery object
    const submitButton = $("#submit");

    // Configure success audio
    let successAudio = document.getElementById("success-audio");
    successAudio.volume = 0.1;

    // Disable the submit button
    submitButton.prop("disabled", true);

    // Progress Bar
    let options = {
        from: {color: "#28b062"},
        to: {color: "#d74f4f"},
        text: {
            value: "0",
            style: {
                color: "#fff",
                position: "absolute",
                left: "50%",
                top: "50%",
                padding: 0,
                margin: 0,
                transform: {
                    prefix: true,
                    value: "translate(-50%, -50%)"
                }
            },
        },
        step: function (state, bar, _) {
            bar.path.setAttribute("stroke", state.color);
            bar.setText(toDecimalPlace(DURATION_OF_THE_CHALLENGE * (1 - bar.value()), 2) + "s");
        },
        strokeWidth: 10,
        easing: "linear",
        duration: DURATION_OF_THE_CHALLENGE * 1000,  // 10 min 30 s
        trailColor: "#555",
        trailWidth: 1,
        svgStyle: {width: "100%", height: "100%"},
        warnings: true
    };

    let progressBar = new ProgressBar.Line("#loading-bar", options);

    // Get the number of questions
    const noQuestions = QUESTIONS_AND_ANSWERS.questions.length

    // Define functions
    function buildQuiz() {
        // Variable to store output
        let output = []; // Empty array

        // Add questions to the output
        for (let q = 0; q < noQuestions; q++) {
            // Get the essential info from the JSON object
            let questionNo = q + 1;
            let question = QUESTIONS_AND_ANSWERS.questions[q];
            let inputFieldPrefixes = QUESTIONS_AND_ANSWERS.prefixes[q];

            // For each prefix, make a new input field
            let inputFields = [];
            inputFieldPrefixes.forEach((prefix, inputFieldNo) => {
                let inputField = `<div class="input-field"><span>${prefix} </span><input class="math-input" id="question_${questionNo}-iField_${inputFieldNo}" type="text" placeholder="Your answer here"><div id="question_${questionNo}-iField_${inputFieldNo}-mathDisplay">$$$$</div></div>`
                inputFields.push(inputField);
            });

            // Check if the current question is the special question 8
            let slideContent = `<div class="slide">`
            if (questionNo === 8) {
                // Add the image above the slide content
                slideContent += `<img id="q8-img" src="${Q8_IMAGE_SOURCE}?${Date.now()}" alt="Question 8 Image">`
            }

            // Add this question and its input fields to the output
            slideContent += `<div class="question"><strong>Question ${questionNo}.</strong> ${question}</div><br><div class="input-fields">${inputFields.join("")}</div></div>`
            output.push(slideContent)
        }

        // Finally combine our output list into one string of HTML and put it on the page
        questionContainer.innerHTML = output.join("");
    }

    function showSlide(n) {
        // Make the desired slide active
        slides[currentSlide].classList.remove("active-slide");
        slides[n].classList.add("active-slide");

        // Change the height of the `body-container` element to the height of the current question
        $(".question-container").height($(".active-slide").height());

        // Update the `currentSlide`
        currentSlide = n;
    }

    function showNextSlide() {
        showSlide(currentSlide + 1);
    }

    function showPreviousSlide() {
        showSlide(currentSlide - 1);
    }

    // Build quiz
    buildQuiz();

    // Pagination
    const slides = $.find(".slide");
    let currentSlide = 0;

    // Prepare input fields' math displays
    function prepareInputFields() {
        // Get all display boxes
        let mjDisplayBoxes = {};
        for (let q = 0; q < noQuestions; q++) {
            let inputFieldPrefixes = QUESTIONS_AND_ANSWERS.prefixes[q];
            inputFieldPrefixes.forEach((prefix, inputFieldNo) => {
                MathJax.Hub.Queue(() => {
                    mjDisplayBoxes[`question_${q + 1}-iField_${inputFieldNo}-mathDisplay`] = MathJax.Hub.getAllJax(`question_${q + 1}-iField_${inputFieldNo}-mathDisplay`)[0];
                });
            });
        }

        // "Live update" MathJax whenever a key is pressed
        $(".math-input").on("keyup", (event) => { // When a keyboard key has been hit & the finger is removed, this code will run
            let target = event.target;
            let math = $(target).val(); // This gets the value of the inputted string
            $(target).css("color", "black"); // Set the string's colour to black

            // Get the id of the element
            if (math.length > 0) { // If there is something typed in
                try {
                    let tree = MathLex.parse(math); // Try to parse the math
                    let latex = MathLex.render(tree, "latex"); // Render the math as latex

                    MathJax.Hub.Queue(["Text", mjDisplayBoxes[target.id + "-mathDisplay"], latex]);
                } catch (err) {
                    $(target).css("color", "red");
                }

            } else {
                // Clear display and output boxes if input is empty
                MathJax.Hub.Queue(["Text", mjDisplayBoxes[target.id + "-mathDisplay"], ""]);
            }
        });
    }

    prepareInputFields();

    // Prepare Submit button functionality
    submitButton.on("click", () => {
        // Get the number of input fields for the current question
        let currentPrefixes = QUESTIONS_AND_ANSWERS.prefixes[currentSlide];
        let noInputFields = currentPrefixes.length;

        // Form the input fields' ids
        let inputFieldsIDs = [];
        for (let i = 0; i < noInputFields; i++) {
            inputFieldsIDs.push(`question_${currentSlide + 1}-iField_${i}`);
        }

        // Get data from the input fields
        let userAnswer = [];
        let checkAnswer = true;

        inputFieldsIDs.forEach((id) => {
            let selector = $("#" + id);
            let math = selector.val();

            if (math.length > 0) {
                try {
                    // Parse the math input into latex
                    let tree = MathLex.parse(math);
                    let latexCode = MathLex.render(tree, "latex");

                    // Put the latex code into an array
                    userAnswer.push(latexCode);

                } catch (err) {
                    // Don't do anything
                }
            } else {
                // Add a class that defines the shaking animation
                selector.addClass("error");

                // Remove the class after the animation completes
                setTimeout(() => {
                    selector.removeClass("error");
                }, 300);  // 300 ms

                // Change the flag of whether to check answers to false
                checkAnswer = false;
            }
        });

        // Submit latex value to server
        if (checkAnswer) {
            $.get("/secret/check-answer", {
                key: "CHECK",
                question_no: currentSlide + 1,
                user_answer: userAnswer
            }, (output) => {
                let isCorrect = output["correct"];
                if (isCorrect) {
                    if (currentSlide + 1 === 14) {  // The last slide
                        let timeLeft = DURATION_OF_THE_CHALLENGE * (1 - progressBar.value());
                        $.get("/secret/success-handler", {
                            key: "a-winner-is-you",
                            user_id: getUUIDCookie(),
                            time_remaining: timeLeft
                        }, (output) => {
                            window.location.replace(output);
                        });
                    } else {
                        // Play success audio
                        successAudio.play();

                        // Move on to next question
                        showNextSlide();
                    }
                } else {
                    // Make all bars shake
                    inputFieldsIDs.forEach((id) => {
                        let selector = $("#" + id);
                        selector.addClass("error");
                        setTimeout(() => {
                            selector.removeClass("error");
                        }, 300);
                    });
                }
            });
        }

    });

    // Show the first slide
    MathJax.Hub.Register.StartupHook("End", async function () {
        showSlide(currentSlide);

        // Audio
        let myAudio = document.getElementById("audio");  // Get the DOM element
        if (myAudio.currentTime < 5) {
            myAudio.currentTime = 5;
        }
        myAudio.play();

        // Start the progress bar
        progressBar.animate(1.0);

        // Activate submit button
        submitButton.prop("disabled", false);

        // Run Async functions
        let sleepFunc = asyncSleep(DURATION_OF_THE_CHALLENGE);  // Start the sleep counter
        await sleepFunc;  // If timer has yet to expire, wait until timer expires

        // If the user can't complete The Challenge in time, bring the user back to the home page
        $.get("/secret/failure", {key: "fail"}, (output) => {
            window.location.replace(output);
        });
    });
});
