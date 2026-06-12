document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {

        let name = document.querySelector('input[name="name"]').value.trim();
        let email = document.querySelector('input[name="email"]').value.trim();
        let complaint = document.querySelector('textarea[name="complaint"]').value.trim();

        if (name === "" || email === "" || complaint === "") {
            alert("Please fill all required fields!");
            event.preventDefault();
            return;
        }

        if (!email.includes("@")) {
            alert("Please enter a valid email address!");
            event.preventDefault();
            return;
        }

        alert("Complaint Submitted Successfully!");
    });

});
function toggleMenu() {
    var menu = document.getElementById("mobileMenu");
    
    
    if (menu.style.display === "flex") {
        menu.style.display = "none";
    } else {
        menu.style.display = "flex";
    }
}