function checkIfCookiesAreEnabled() {
    // Check if can directly see if a cookie can be set
    if (navigator.cookieEnabled) return true;

    // If not, manually set and read a cookie
    document.cookie = "cookie_test=1";
    let ret = document.cookie.indexOf("cookie_test=") !== -1;

    // Delete the cookie
    document.cookie = "cookie_test=1; expires=Thu, 01-Jan-1970 00:00:00 GMT";

    // Return test result
    return ret;
}

function checkIfWindowSizeOkay() {
    return $(window).width() >= 720;
}

async function checkIfCanStartTheChallenge() {
    // Check if cookies are enabled
    let cookiesEnabled = checkIfCookiesAreEnabled();

    // Check if the screen width is acceptable
    let windowSizeOkay = checkIfWindowSizeOkay();

    // Check if user is online
    let isOnline = await checkIfOnline();

    // Show an appropriate error message for each case
    let errorText = $("#js--error-text");

    if (!isOnline) {
        errorText.html("You cannot play The Challenge if you are offline.");
    } else if (!cookiesEnabled) {
        errorText.html("You cannot play The Challenge if cookies are not enabled.");
    } else if (!windowSizeOkay) {
        errorText.html("You cannot play The Challenge when the screen width is too small.");
    } else {
        errorText.html("");  // Clear the text field
    }

    // Check if can start the challenge
    return !(!isOnline || !cookiesEnabled || !windowSizeOkay);
}

$(document).ready(async () => {
    // Disable button first
    document.getElementById("js--start-button").disabled = true;

    // Create a click event for the start button
    $("#js--start-button").on("click", () => {
        console.log("Start button clicked.");
        $.get("/secret/start-challenge", {key: generateOTP("START2CHALLENGE3")}, (output) => {
            console.log(output);
            window.location.replace(output);
        });
    });

    // Handle sticky navigation
    $(".information-box").waypoint((direction) => {
        if (direction === "down") {
            $("nav").addClass("sticky");
        } else {
            $("nav").removeClass("sticky");
        }
    });

    // Scroll handlers
    $("#js--scroll-to-practice-questions").click(() => {
        // Get nav element
        let nav = $("#js--nav");

        // Calculate offset amount based on height of navigation element
        let offsetAmount = Math.ceil(nav.height());

        // Deal with the annoying case that when the nav element is more than 900 px and it is not sticky
        if (nav.width() > 900 && !nav.hasClass("sticky")) {
            offsetAmount -= 40;
        }

        // Scroll to the perfect height
        $("html, body").animate({scrollTop: $("#js--practice-questions").offset().top - offsetAmount});
    });

    // Handle clicking of menu icon
    $("#js--nav-icon").click(function () {
        let nav = $(".main-nav");
        let icon = $("#js--nav-icon i");

        nav.slideToggle(200);

        if (icon.hasClass("ion-navicon-round")) {
            icon.addClass("ion-close-round");
            icon.removeClass("ion-navicon-round");
        } else {
            icon.addClass("ion-navicon-round");
            icon.removeClass("ion-close-round");
        }
    });

    // Check if start button should be enabled
    if (await checkIfCanStartTheChallenge()) {
        console.log("Acceptable conditions; enabling button.");
        document.getElementById("js--start-button").disabled = false;
    } else {
        console.log("Unacceptable conditions; button continuing to be disabled.")
    }

    // Create a resize event
    $(window).resize(async () => {
        // Check if can re-enable the start button
        if (!(await checkIfCanStartTheChallenge())) {
            console.log("[AFTER RESIZE] Unacceptable conditions; disabling button.");
            document.getElementById("js--start-button").disabled = true;
        } else {
            console.log("[AFTER RESIZE] Acceptable conditions; enabling button.");
            document.getElementById("js--start-button").disabled = false;
        }
    });
});
