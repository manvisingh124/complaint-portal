document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    
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

            
            if (window.location.pathname.includes("complaint.html")) {
                let randomID = "BBDU-" + Math.floor(1000 + Math.random() * 9000);
                alert("Complaint Submitted Successfully!\n\nYour Complaint ID is: " + randomID + "\n\nPlease note down this ID to track status.");
            } else {
                
                alert("Complaint Submitted Successfully!");
            }
        });
    }

    
    if (window.location.pathname.includes("status.html")) {
        const statusInput = document.querySelector("input[type='text']");
        const statusBtn = document.querySelector("input[type='submit']") || document.querySelector("button");

        if (statusBtn && statusInput) {
            statusBtn.addEventListener("click", function (event) {
                event.preventDefault(); 
                
                let enteredID = statusInput.value.trim();

                if (enteredID === "") {
                    alert("Please enter a valid Complaint ID!");
                    return;
                }

            
                alert("Status for ID (" + enteredID + "):\n\nYour complaint has been received and it is currently 'UNDER PROCESS' by the University Administration.");
            });
        }
    }

});


function toggleMenu() {
    
    var menu = document.getElementById("dropdownMenu");
    
    if (menu) {
        menu.classList.toggle("hide");
    }
}