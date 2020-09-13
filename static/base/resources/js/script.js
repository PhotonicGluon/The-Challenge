// GLOBAL FUNCTIONS (Functions that are available to all JS files)
function create_alert(alert_info, parent_element=document.body) {
    // Craft alert HTML
    let alertHTML = `<div class="alert"><span class="alert-box-close-button" id="alert-temp">&times;</span>${alert_info}</div>`;

    // Prepend the HTML code to the `parent_element`
    parent_element.insertAdjacentHTML("afterbegin", alertHTML);

    // Get the new alert close button element
    let alertCloseButton = document.getElementById("alert-temp");

    // Remove the id from the alert close button element
    alertCloseButton.removeAttribute("id");

    // Add an 'onclick' event to the alert
    alertCloseButton.onclick = function () {
        // Get the div element of the alert
        let div = this.parentElement;

        // Set the opacity of div to 0%
        div.style.opacity = "0";

        // Wait for 600 ms before executing this code
        setTimeout(function () {
            // Hide the div
            div.style.display = "none";

            // Remove the div after the `div`'s display has been set to "none".
            div.remove()
        }, 600);
    }
}


function getUUIDCookie() {
    // Get all pairs of cookies in the browser
    let pairs = document.cookie.split(";");

    // Get all cookies' names
    let cookies = {};
    for (let i=0; i<pairs.length; i++){
        let pair = pairs[i].split("=");
        cookies[(pair[0]+ "").trim()] = unescape(pair.slice(1).join("="));
    }

    // Get the UUID
    return cookies["ChallengeUUID"];
}

function toSignificance(x, precision) {
  return Number.parseFloat(x).toPrecision(precision);
}

function toDecimalPlace(x, decimalPlace) {
  return Number.parseFloat(x).toFixed(decimalPlace);
}

async function asyncSleep(timeInSeconds) {
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve("Slept for " + timeInSeconds * 1000 + " seconds"), timeInSeconds * 1000)
    });
    await promise; // wait until the promise resolves (*)
    return 1;
}

// BASE CODE (JS code that will run on every page on The Challenge)
// Setup alert system
let close = document.getElementsByClassName("alert-box-close-button")

// Loop through all close buttons
for (let i = 0; i < close.length; i++) {
    // When someone clicks on a close button
    close[i].onclick = function () {

        // Get the parent of the close button element (the div element)
        let div = this.parentElement;

        // Set the opacity of div to 0%
        div.style.opacity = "0";

        // Wait for 600 ms before executing this code
        setTimeout(function () {
            // Hide the div
            div.style.display = "none";

            // Remove the div after the `div`'s display has been set to `none`.
            div.remove()
        }, 600);
    }
}

// Setup heartbeat system
let socket = io();  // Setup SocketIO port
let uniqueID = getUUIDCookie();

socket.emit("Heartbeat", {uuid: uniqueID});
setInterval(() => {
    socket.emit("Heartbeat", {uuid: uniqueID});
}, 120 * 1000);  // Perform a heartbeat every 120 seconds
