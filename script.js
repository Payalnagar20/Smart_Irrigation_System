// Get references to elements
const signUpContainer = document.getElementById('signup');
const signInContainer = document.getElementById('signIn');
const signInButton = document.getElementById('signInButton');
const signUpButton = document.getElementById('signUpButton');
const submitSignUp = document.getElementById('submitSignUp');
const submitSignIn = document.getElementById('submitSignIn');
const signupForm = document.getElementById('signupForm');
const signinForm = document.getElementById('signinForm');
const signUpMessage = document.getElementById('signUpMessage');
const signInMessage = document.getElementById('signInMessage');

// Toggle between sign-up and sign-in forms
signInButton.addEventListener('click', () => {
    signUpContainer.style.display = 'none';
    signInContainer.style.display = 'block';
    signUpMessage.style.display = 'none';
    signInMessage.style.display = 'none';
});

signUpButton.addEventListener('click', () => {
    signInContainer.style.display = 'none';
    signUpContainer.style.display = 'block';
    signUpMessage.style.display = 'none';
    signInMessage.style.display = 'none';
});

// Sign Up
submitSignUp.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent form submission
    signUpMessage.style.display = 'block';
    signUpMessage.textContent = "Sign-up logic goes here (e.g., Firebase, backend)";

    // ***Placeholder - Replace with your actual sign-up logic***
    // This example only shows basic client-side validation.
    // In a real application, you would send data to your backend
    // for user creation and authentication.

    // Example (very basic validation):
    const fName = document.getElementById('fName').value;
    const lName = document.getElementById('lName').value;
    const rEmail = document.getElementById('rEmail').value;
    const rPassword = document.getElementById('rPassword').value;

    if (fName.trim() === "" || lName.trim() === "" || rEmail.trim() === "" || rPassword.trim() === "") {
        signUpMessage.textContent = "Please fill in all fields.";
        return; // Stop further execution
    }

    // If validation passes (replace with your backend logic)
    // Example: redirect after successful sign-up (replace with your logic)
    // window.location.href = "web.html"; // Redirect to your main page

});

// Sign In
submitSignIn.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const signInMessage = document.getElementById('signInMessage');

    signInMessage.style.display = 'block';
    signInMessage.textContent = "Signing in...";


    if (email.trim() !== "" && password.trim() !== "") {
        signInMessage.style.display = 'none'; // Hide the message
        window.location.href = 'web.html'; // Redirect to your main page
    } else {
        signInMessage.textContent = 'Please enter email and password.';
    }

});