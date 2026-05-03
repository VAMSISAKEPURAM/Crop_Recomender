document.addEventListener('DOMContentLoaded', () => {
    // --- Dark Mode Logic ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');
    
    // Check local storage or system preference
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateIcons(currentTheme);
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateIcons('dark');
    }

    if(themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            let targetTheme = 'light';
            if (document.documentElement.getAttribute('data-theme') !== 'dark') {
                targetTheme = 'dark';
            }
            document.documentElement.setAttribute('data-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
            updateIcons(targetTheme);
        });
    }

    function updateIcons(theme) {
        if (!sunIcon || !moonIcon) return;
        if (theme === 'dark') {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        }
    }

    // --- Prediction Form AJAX ---
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');
    const cropNameDisplay = document.getElementById('crop-name');
    const cropDetailsDisplay = document.getElementById('crop-details');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn ? submitBtn.querySelector('.btn-text') : null;
    const loader = submitBtn ? submitBtn.querySelector('.loader') : null;

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Hide previous results
            resultContainer.style.display = 'none';
            errorContainer.style.display = 'none';
            
            // Show loading state
            if(btnText && loader) {
                btnText.style.display = 'none';
                loader.style.display = 'block';
                submitBtn.disabled = true;
            }

            // Gather data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    cropNameDisplay.textContent = result.prediction;
                    cropDetailsDisplay.textContent = `The AI model analyzed your soil and climate data, maintaining a high recommendation confidence for ${result.prediction}. Optimal next steps include consulting local seed variants and soil preparation mechanisms specific for this crop.`;
                    resultContainer.style.display = 'block';
                } else {
                    errorMessage.textContent = result.error || 'An unexpected error occurred.';
                    errorContainer.style.display = 'block';
                }
            } catch (error) {
                console.error("Fetch Error:", error);
                errorMessage.textContent = 'Failed to connect to the server. Please check your network connection and try again.';
                errorContainer.style.display = 'block';
            } finally {
                // Restore button state
                if(btnText && loader) {
                    btnText.style.display = 'block';
                    loader.style.display = 'none';
                    submitBtn.disabled = false;
                }
            }
        });
    }
});

// Global reset function
window.resetForm = function() {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');
    
    if(form) form.reset();
    if(resultContainer) resultContainer.style.display = 'none';
    if(errorContainer) errorContainer.style.display = 'none';
    
    // Focus first input
    const firstInput = document.getElementById('N');
    if(firstInput) firstInput.focus();
};
