$(document).ready(() => {
    // Get the display box
    let mjDisplayBox = null;
    MathJax.Hub.Queue(() => {
        mjDisplayBox = MathJax.Hub.getAllJax("js--math-display")[0];
    });

    // Get the input field
    let inputField = $("#input-field");

    // "Live update" the display box and the latex output whenever a key is pressed
    inputField.on("keyup", (event) => {  // When a keyboard key has been hit & the finger is removed, this code will run
        let target = event.target;
        let math = $(target).val();  // This gets the value of the inputted string
        $(target).css("color", "black");  // Set the string's colour to black

        // Get the id of the element
        if (math.length > 0) {  // If there is something typed in
            try {
                // Get latex form of the math input
                let tree = MathLex.parse(math);  // Try to parse the math
                let latex = MathLex.render(tree, "latex");  // Render the math as latex

                // Output the latex code to the span element
                $("#js--latex-output").text(latex);

                // Render the latex code using MathJax
                MathJax.Hub.Queue(["Text", mjDisplayBox, latex]);

            } catch (err) {
                console.log(err);
                $(target).css("color", "red");
            }

        } else {
            // Clear display and output boxes if input is empty
            $("#latex-output").text("");
            MathJax.Hub.Queue(["Text", mjDisplayBox, ""]);
        }
    });

    // Perform a fake keyup event to trigger the equation rendering
    setTimeout(() => inputField.keyup(), 1000);
});
