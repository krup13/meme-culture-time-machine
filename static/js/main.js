document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality
    const navTabs = document.querySelectorAll('.nav-tab');
    const sections = document.querySelectorAll('.section');
    
    navTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs and hide all sections
            navTabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.style.display = 'none');
            
            // Add active class to clicked tab and show corresponding section
            const tabName = this.getAttribute('data-tab');
            this.classList.add('active');
            document.getElementById(tabName + '-section').style.display = 'block';
        });
    });
    
    // Era theme switching
    const eraTabs = document.querySelectorAll('.era-tab');
    
    function applyEraTheme(era) {
        // Remove all era classes
        document.body.classList.remove('era-1990s', 'era-2000s', 'era-2010s', 'era-2020s');
        
        // Add the selected era class
        document.body.classList.add(`era-${era}`);
        
        // Update active tab
        eraTabs.forEach(tab => {
            if (tab.getAttribute('data-era') === era) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });
        
        // Update era select dropdown if it exists
        const eraSelect = document.getElementById('era-select');
        if (eraSelect) {
            eraSelect.value = era;
        }
        
        // Store the selected era in localStorage for persistence
        localStorage.setItem('selectedEra', era);
        
        console.log(`Theme applied: era-${era}`);
    }
    
    // Set initial theme from localStorage or default to 2000s
    const savedEra = localStorage.getItem('selectedEra') || '2000s';
    console.log("Initial era:", savedEra);
    applyEraTheme(savedEra);
    
    // Add click event listeners to era tabs
    eraTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const selectedEra = this.getAttribute('data-era');
            console.log("Era tab clicked:", selectedEra);
            applyEraTheme(selectedEra);
        });
    });
    
    // Update theme when select dropdown changes
    const eraSelect = document.getElementById('era-select');
    if (eraSelect) {
        eraSelect.addEventListener('change', function() {
            console.log("Era select changed:", this.value);
            applyEraTheme(this.value);
        });
    }
    
    // File upload handling
    const uploadBtn = document.getElementById('upload-btn');
    const imageInput = document.getElementById('image-input');
    
    if (uploadBtn && imageInput) {
        uploadBtn.addEventListener('click', function() {
            imageInput.click();
        });
        
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Preview the selected image
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'responsive-image';
                    
                    const imageBox = document.querySelector('.image-box:first-child');
                    if (imageBox) {
                        imageBox.innerHTML = '';
                        imageBox.appendChild(img);
                    }
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Form submission handling
    const translateBtn = document.getElementById('translate-btn');
    // Update the translate button event handler with better error handling
    if (translateBtn) {
        translateBtn.addEventListener('click', function() {
            const textInput = document.getElementById('text-input');
            const eraSelect = document.getElementById('era-select');
            
            if (!textInput || !eraSelect) {
                console.error('Required elements not found');
                return;
            }
            
            const text = textInput.value;
            const era = eraSelect.value;
            
            if (text.trim() === '') {
                alert('Please enter some text to translate.');
                return;
            }
            
            // Show loading state
            const resultElement = document.getElementById('translation-result');
            if (resultElement) {
                resultElement.innerHTML = '<p>Translating...</p>';
            }
            
            console.log(`Sending translation request for era: ${era}`);
            
            // Here you would add the API call to your backend
            fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text, era: era })
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json().then(data => {
                    if (!response.ok) {
                        throw new Error(data.error || `HTTP error! Status: ${response.status}`);
                    }
                    return data;
                });
            })
            .then(data => {
                console.log('Translation success:', data);
                if (resultElement) {
                    if (data.error) {
                        resultElement.innerHTML = `<div class="error-message">${data.error}</div>`;
                    } else {
                        // Apply proper styling to the translated text
                        resultElement.innerHTML = `<div class="translated-text">${data.translated}</div>`;
                        
                        // Update cringe meter
                        const meter = document.querySelector('.meter-fill');
                        if (meter) {
                            meter.style.width = `${data.cringe_score}%`;
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error during translation:', error);
                if (resultElement) {
                    resultElement.innerHTML = `<div class="error-message">Server error: ${error.message || 'Could not translate text'}</div>`;
                }
            });
        });
    }
});
