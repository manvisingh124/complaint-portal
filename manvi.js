document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    // Agar kisi page par form na ho (jaise Home page), toh error na aaye isliye check kiya
    if (form) {
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
    }

});

// Naya aur updated toggleMenu function jo smoothly dropdown chalayega
function toggleMenu() {
    // Humne HTML me id="dropdownMenu" rakha tha, usey fetch kiya
    var menu = document.getElementById("dropdownMenu");
    
    if (menu) {
        // Agar '.hide' class pehle se hai toh hata dega (menu khul jayega)
        // Aur agar nahi hai toh jod dega (menu band ho jayega)
        menu.classList.toggle("hide");
    }
}