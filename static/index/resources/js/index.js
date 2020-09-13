function checkWindowSize() {
    if ($(window).width() < 720) {
        $("#mobile-error").html("You cannot play The Challenge on mobile.");
        return false;
    } else {
        $("#mobile-error").html("");  // Clear it
        return true;
    }
}

function checkIfCookieEnabled() {
    if (navigator.cookieEnabled) return true;

    // Set and read a cookie
    document.cookie = "cookie_test=1";
    let ret = document.cookie.indexOf("cookie_test=") !== -1;

    // delete cookie
    document.cookie = "cookie_test=1; expires=Thu, 01-Jan-1970 00:00:01 GMT";

    return ret;
}

$(document).ready(() => {
    // Create a start-game variable
    let canStartGame = true;

    // Check if cookies are enabled and, if not, disable the start button
    let cookieEnabled = checkIfCookieEnabled();

    if (!cookieEnabled) {
        canStartGame = false;
        create_alert("Cookies must be enabled to play The Challenge.")
    }

    // Check screen size
    let acceptableWindowSize = checkWindowSize();

    // Check if start button is disabled
    if (!cookieEnabled || !acceptableWindowSize) {
        document.getElementById("start-button").disabled = true;
    }

    // Create a click event for the start button
    $("#start-button").on("click", () => {
        console.log("Start button clicked.")
        $.get("/secret/start_challenge", {key: "μυστικό"}, (output) => {
            window.location.replace(output);
        });
    });

    // Create a resize event
    $(window).resize(() => {
        // Check window size
        let acceptableWindowSize = checkWindowSize();

        // Check if can start game
        document.getElementById("start-button").disabled = !cookieEnabled || !acceptableWindowSize;
    });
});
