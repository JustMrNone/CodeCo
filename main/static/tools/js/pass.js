document.addEventListener("DOMContentLoaded", function() {
    const passwordForm = document.getElementById('password-form');
    const passwordLengthInput = document.getElementById('password-length');
    const passwordLengthDisplay = document.getElementById('password-length-display');
    const includeLowercase = document.getElementById('include-lowercase');
    const includeUppercase = document.getElementById('include-uppercase');
    const includeDigits = document.getElementById('include-digits');
    const includeSpecial = document.getElementById('include-special');
    const generatedPassword = document.getElementById('generated-password');

    // Update length display when slider is moved
    passwordLengthInput.addEventListener('input', function() {
        passwordLengthDisplay.textContent = passwordLengthInput.value;
    });

    // Function to generate password
    function generatePassword(length, useLower, useUpper, useDigits, useSpecial) {
        const lowerCaseChars = 'abcdefghijklmnopqrstuvwxyz';
        const upperCaseChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const digitChars = '0123456789';
        const specialChars = '!@#$%^&*()_+[]{}|;:,.<>?';

        let charSet = '';
        if (useLower) charSet += lowerCaseChars;
        if (useUpper) charSet += upperCaseChars;
        if (useDigits) charSet += digitChars;
        if (useSpecial) charSet += specialChars;

        if (charSet === '') return '';

        let password = '';
        for (let i = 0; i < length; i++) {
            const randomIndex = Math.floor(Math.random() * charSet.length);
            password += charSet[randomIndex];
        }
        return password;
    }

    // Form submission handler
    passwordForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const length = parseInt(passwordLengthInput.value);
        const useLower = includeLowercase.checked;
        const useUpper = includeUppercase.checked;
        const useDigits = includeDigits.checked;
        const useSpecial = includeSpecial.checked;

        const password = generatePassword(length, useLower, useUpper, useDigits, useSpecial);
        generatedPassword.value = password;
    });
});