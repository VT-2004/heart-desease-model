document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input, select');

    // Define validation rules - must match server-side rules for consistency
    const validationRules = {
        age: {min: 1, max: 120, message: "Age must be between 1 and 120 years."},
        trestbps: {min: 80, max: 200, message: "Resting Blood Pressure must be between 80 and 200 mm Hg."},
        chol: {min: 100, max: 600, message: "Serum Cholestoral must be between 100 and 600 mg/dl."},
        thalach: {min: 60, max: 220, message: "Max Heart Rate must be between 60 and 220 bpm."},
        oldpeak: {min: 0.0, max: 6.2, message: "ST Depression must be between 0.0 and 6.2."},
        sex: {allowed: ['0', '1'], message: "Please select a valid Sex option."},
        cp: {allowed: ['1', '2', '3', '4'], message: "Please select a valid Chest Pain Type."},
        fbs: {allowed: ['0', '1'], message: "Please select a valid Fasting Blood Sugar option."},
        restecg: {allowed: ['0', '1', '2'], message: "Please select a valid Resting ECG result."},
        exang: {allowed: ['0', '1'], message: "Please select a valid Exercise Induced Angina option."},
        slope: {allowed: ['1', '2', '3'], message: "Please select a valid Slope option."},
        ca: {allowed: ['0', '1', '2', '3'], message: "Please select a valid Number of Major Vessels (0-3)."},
        thal: {allowed: ['3', '6', '7'], message: "Please select a valid Thalassemia option."}
    };

    function validateInput(inputElement) {
        const fieldName = inputElement.id;
        const value = inputElement.value;
        const rules = validationRules[fieldName];
        let isValid = true;
        let errorMessage = '';

        // Check if the input is required and empty (HTML5 'required' handles this too, but good to double check)
        if (inputElement.hasAttribute('required') && value.trim() === '') {
            isValid = false;
            errorMessage = `${inputElement.labels[0].textContent.replace(':', '').trim()} is required.`;
        } else if (rules) {
            // Numeric validation
            if (inputElement.type === 'number') {
                const numValue = parseFloat(value);
                if (isNaN(numValue)) {
                    isValid = false;
                    errorMessage = "Please enter a valid number.";
                } else if (rules.min !== undefined && numValue < rules.min) {
                    isValid = false;
                    errorMessage = rules.message;
                } else if (rules.max !== undefined && numValue > rules.max) {
                    isValid = false;
                    errorMessage = rules.message;
                }
            }
            // Select/Categorical validation
            else if (inputElement.tagName === 'SELECT') {
                if (rules.allowed && !rules.allowed.includes(value)) {
                    isValid = false;
                    errorMessage = rules.message;
                }
            }
        }

        // Display error message
        const errorSpan = inputElement.nextElementSibling; // Assuming error span is right after input
        if (errorSpan && errorSpan.classList.contains('error-message-client')) {
            if (!isValid) {
                errorSpan.textContent = errorMessage;
                errorSpan.style.display = 'block';
                inputElement.classList.add('input-error'); // Add error class to input
            } else {
                errorSpan.textContent = '';
                errorSpan.style.display = 'none';
                inputElement.classList.remove('input-error'); // Remove error class
            }
        }
        return isValid;
    }

    // Add event listeners for real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', function() { // Validate on input change
            validateInput(this);
        });
        input.addEventListener('blur', function() { // Validate when input loses focus
            validateInput(this);
        });
    });

    // Validate all inputs on form submission
    form.addEventListener('submit', function(event) {
        let formIsValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) {
                formIsValid = false;
            }
        });

        if (!formIsValid) {
            event.preventDefault(); // Prevent form submission if client-side validation fails
            alert('Please correct the highlighted errors before submitting.'); // Optional alert
        }
    });
});