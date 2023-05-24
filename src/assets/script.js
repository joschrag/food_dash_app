function applyStylesToElement(attempts) {
    var element = document.querySelector('.daq-colorpicker--dark__container');
    console.log(element);
    if (element) {
        for (let index = 0; index < element.classList.length; index++) {
            const class_str = element.classList[index];
            console.log(class_str);
            var class_el = document.querySelector(".".concat("", class_str));
            console.log(class_el.style);
            class_el.setAttribute("style", "box-shadow: none !important")
        }
        return; // Stop the script execution
    }

    if (attempts >= 10) {
        return; // Stop the script execution after 10 unsuccessful attempts
    }

    // If the element is not found, wait for 500 milliseconds and try again
    setTimeout(function () {
        applyStylesToElement(attempts + 1); // Increase the attempts counter
    }, 500);
}

window.addEventListener('load', function () {
    applyStylesToElement(0); // Start the recursive function with 0 attempts
});
