async function loadQuestions() {
    let promise = new Promise((resolve, reject) => {
        $.get("/secret/setup-questions", {key: generate_otp("SETUP2QUESTIONS3")}, (output) => {
            console.log(output);
            resolve(output);
        });
    });
    await promise;
    console.log("Questions loaded");
}

$(document).ready(async () => {
    // Audio
    let myAudio = document.getElementById("js--audio-loading");
    myAudio.play();

    // Progress Bar
    let options = {
        from: {
            color: "#28b062"
        },
        to: {color: "#28b062"},
        step: function (state, bar, _) {
            bar.path.setAttribute("stroke", state.color);
        },
        strokeWidth: 10,
        easing: "easeInOut",
        duration: 5000,
        trailColor: "#ddd",
        trailWidth: 1,
        svgStyle: {width: "100%", height: "100%"},
        warnings: true
    };

    let progressBar = new ProgressBar.Line("#js--loading-bar", options);
    progressBar.animate(1.0);

    // Run Async functions
    let sleepFunc = asyncSleep(5);  // Start the sleep counter
    await loadQuestions();  // Wait till the questions are loaded
    await sleepFunc;  // If timer has yet to expire, wait until timer expires
    console.log("Done!");

    // Redirect to question pages
    console.log("Redirecting to question pages.")
    $.get("/secret/redirect-to-the-challenge", {key: generate_otp("REDIRECTING2TO3THE4CHALLENGE5NOW")}, (output) => {
        window.location.replace(output);
    });
});
