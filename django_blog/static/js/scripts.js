// Script for handling authentication forms and UI interactions
document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog page loaded');
    
    // Form validation for login and registration
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredInputs = form.querySelectorAll('input[required]');
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error-input');
                    
                    // Create error message if it doesn't exist
                    let errorMsg = input.parentNode.querySelector('.error-message');
                    if (!errorMsg) {
                        errorMsg = document.createElement('div');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'This field is required';
                        input.parentNode.appendChild(errorMsg);
                    }
                } else {
                    input.classList.remove('error-input');
                    const errorMsg = input.parentNode.querySelector('.error-message');
                    if (errorMsg) {
                        errorMsg.remove();
                    }
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    });
    
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(() => {
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 5000);
    }
});