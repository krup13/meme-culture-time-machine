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
    
    // Era tab switching
    const eraTabs = document.querySelectorAll('.era-tab');
    
    eraTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            eraTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const selectedEra = this.getAttribute('data-era');
            // Here you would add code to update the app content based on selected era
            document.getElementById('era-select').value = selectedEra;
        });
    });
    
    // File upload handling
    const uploadBtn = document.getElementById('upload-btn');
    const imageInput = document.getElementById('image-input');
    
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
                imageBox.innerHTML = '';
                imageBox.appendChild(img);
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    // Form submission handling
    const translateBtn = document.getElementById('translate-btn');
    translateBtn.addEventListener('click', function() {
        const textInput = document.getElementById('text-input').value;
        const era = document.getElementById('era-select').value;
        
        if (textInput.trim() === '') {
            alert('Please enter some text to translate.');
            return;
        }
        
        // Here you would add the API call to your backend
        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput, era: era })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('translation-result').innerHTML = 
                    `<div class="error-message">${data.error}</div>`;
            } else {
                document.getElementById('translation-result').innerHTML = data.translated;
                // Update cringe meter
                const meter = document.querySelector('.meter-fill');
                meter.style.width = data.cringe_score + '%';
            }
        })
        .catch(error => {
            document.getElementById('translation-result').innerHTML = 
                `<div class="error-message">Server error: ${error}</div>`;
        });
    });
    
    // Similar handlers for transform button, record button, etc.
});
