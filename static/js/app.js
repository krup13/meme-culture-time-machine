document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initTextTranslator();
    initImageTransformer();
    initVoiceConverter();
    initMemeGenerator();
    
    // Initialize navigation
    initNavigation();
});

// Text Translator
function initTextTranslator() {
    const translateBtn = document.getElementById('translate-btn');
    const modernText = document.getElementById('modern-text');
    const translatedTextOutput = document.getElementById('translated-text');
    const textEra = document.getElementById('text-era');
    const cringeLevel = document.querySelector('.cringe-level');
    
    translateBtn.addEventListener('click', async function() {
        if (!modernText.value.trim()) {
            alert('Please enter some text to translate');
            return;
        }
        
        translateBtn.disabled = true;
        translateBtn.textContent = 'Translating...';
        
        try {
            // Call translation API
            const response = await fetchAPI('/translate-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: modernText.value,
                    era: textEra.value
                })
            });
            
            translatedTextOutput.textContent = response.translated_text;
            
            // Get cringe rating for the translated text
            const cringeResponse = await fetchAPI('/rate-cringe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: response.translated_text,
                    era: textEra.value
                })
            });
            
            // Update cringe meter
            const cringePct = (cringeResponse.rating / 10) * 100;
            cringeLevel.style.width = `${cringePct}%`;
            
        } catch (error) {
            console.error('Translation error:', error);
            translatedTextOutput.textContent = 'Error: Could not translate text.';
        } finally {
            translateBtn.disabled = false;
            translateBtn.textContent = 'Translate';
        }
    });
}

// Image Transformer
function initImageTransformer() {
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const transformBtn = document.getElementById('transform-btn');
    const transformedImage = document.getElementById('transformed-image');
    const imageEra = document.getElementById('image-era');
    
    // Preview selected image
    imageInput.addEventListener('change', function(event) {
        if (event.target.files && event.target.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagePreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                transformBtn.disabled = false;
            };
            
            reader.readAsDataURL(event.target.files[0]);
        }
    });
    
    transformBtn.addEventListener('click', async function() {
        if (!imageInput.files || !imageInput.files[0]) {
            alert('Please select an image to transform');
            return;
        }
        
        transformBtn.disabled = true;
        transformBtn.textContent = 'Transforming...';
        
        try {
            const formData = new FormData();
            formData.append('image', imageInput.files[0]);
            formData.append('era', imageEra.value);
            
            const response = await fetchAPI('/transform-image', {
                method: 'POST',
                body: formData
            });
            
            transformedImage.innerHTML = `
                <img src="${response.transformed_url}" alt="Transformed Image">
                <div class="download-link">
                    <a href="${response.transformed_url}" download target="_blank">Download</a>
                </div>
            `;
            
        } catch (error) {
            console.error('Image transformation error:', error);
            transformedImage.innerHTML = 'Error: Could not transform image.';
        } finally {
            transformBtn.disabled = false;
            transformBtn.textContent = 'Transform';
        }
    });
    
    // Add auto-detect era button
    const detectEraBtn = document.createElement('button');
    detectEraBtn.textContent = 'Detect Era';
    detectEraBtn.id = 'detect-era-btn';
    imageEra.parentNode.insertBefore(detectEraBtn, transformBtn);
    
    detectEraBtn.addEventListener('click', async function() {
        if (!imageInput.files || !imageInput.files[0]) {
            alert('Please select an image first');
            return;
        }
        
        detectEraBtn.disabled = true;
        detectEraBtn.textContent = 'Detecting...';
        
        try {
            const formData = new FormData();
            formData.append('image', imageInput.files[0]);
            
            const response = await fetchAPI('/detect-image-era', {
                method: 'POST',
                body: formData
            });
            
            // Update the era dropdown to match detected era
            imageEra.value = response.era;
            
            // Display detection result
            imagePreview.innerHTML += `
                <div class="detection-result">
                    <p>Detected Era: <strong>${response.era}</strong></p>
                </div>
            `;
            
        } catch (error) {
            console.error('Era detection error:', error);
            alert('Could not detect image era');
        } finally {
            detectEraBtn.disabled = false;
            detectEraBtn.textContent = 'Detect Era';
        }
    });
}

// Voice Converter
function initVoiceConverter() {
    const recordBtn = document.getElementById('record-btn');
    const recordingStatus = document.getElementById('recording-status');
    const audioPreview = document.getElementById('audio-preview');
    const convertBtn = document.getElementById('convert-voice-btn');
    const convertedVoice = document.getElementById('converted-voice');
    const voiceEra = document.getElementById('voice-era');
    
    let mediaRecorder;
    let audioChunks = [];
    let audioBlob;
    
    // Set up audio recording
    recordBtn.addEventListener('click', async function() {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            // Start recording
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = function(e) {
                    audioChunks.push(e.data);
                };
                
                mediaRecorder.onstop = function() {
                    audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    
                    audioPreview.innerHTML = `
                        <audio controls src="${audioUrl}"></audio>
                        <p>Recording complete</p>
                    `;
                    
                    recordBtn.classList.remove('recording');
                    recordBtn.querySelector('.record-text').textContent = 'Record Again';
                    recordingStatus.textContent = 'Not recording';
                    convertBtn.disabled = false;
                };
                
                mediaRecorder.start();
                recordBtn.classList.add('recording');
                recordBtn.querySelector('.record-text').textContent = 'Stop Recording';
                recordingStatus.textContent = 'Recording...';
                
            } catch (error) {
                console.error('Recording error:', error);
                alert('Could not access microphone. Please check permissions.');
            }
        } else {
            // Stop recording
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    });
    
    convertBtn.addEventListener('click', async function() {
        if (!audioBlob) {
            alert('Please record audio first');
            return;
        }
        
        convertBtn.disabled = true;
        convertBtn.textContent = 'Converting...';
        
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.mp3');
            formData.append('era', voiceEra.value);
            
            const response = await fetchAPI('/convert-voice', {
                method: 'POST',
                body: formData
            });
            
            convertedVoice.innerHTML = `
                <audio controls src="${response.converted_url}" autoplay></audio>
                <div class="download-link">
                    <a href="${response.converted_url}" download target="_blank">Download</a>
                </div>
            `;
            
        } catch (error) {
            console.error('Voice conversion error:', error);
            convertedVoice.innerHTML = 'Error: Could not convert voice.';
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = 'Convert';
        }
    });
    
    // Add auto-transcription button
    const transcribeBtn = document.createElement('button');
    transcribeBtn.textContent = 'Transcribe';
    transcribeBtn.id = 'transcribe-btn';
    transcribeBtn.disabled = true;
    convertBtn.parentNode.insertBefore(transcribeBtn, convertBtn);
    
    transcribeBtn.addEventListener('click', async function() {
        if (!audioBlob) {
            alert('Please record audio first');
            return;
        }
        
        transcribeBtn.disabled = true;
        transcribeBtn.textContent = 'Transcribing...';
        
        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.mp3');
            
            const response = await fetchAPI('/speech-to-text', {
                method: 'POST',
                body: formData
            });
            
            if (response.transcript) {
                // Create text display
                const transcriptDiv = document.createElement('div');
                transcriptDiv.className = 'transcript';
                transcriptDiv.innerHTML = `
                    <h4>Transcript:</h4>
                    <p>${response.transcript}</p>
                `;
                audioPreview.appendChild(transcriptDiv);
            } else {
                throw new Error('No transcript returned');
            }
            
        } catch (error) {
            console.error('Transcription error:', error);
            alert('Could not transcribe audio');
        } finally {
            transcribeBtn.disabled = false;
            transcribeBtn.textContent = 'Transcribe';
        }
    });
    
    // Enable transcribe button when recording is complete
    mediaRecorder.onstop = function() {
        // ...existing code...
        transcribeBtn.disabled = false;
    };
}

// Meme Generator
function initMemeGenerator() {
    const templateItems = document.querySelectorAll('.template-item');
    const memeImage = document.getElementById('meme-image');
    const memeText = document.getElementById('meme-text');
    const generateBtn = document.getElementById('generate-meme-btn');
    const generatedMeme = document.getElementById('generated-meme');
    const memeHistory = document.getElementById('meme-history');
    const searchYoutubeBtn = document.getElementById('search-youtube-btn');
    const youtubeResults = document.getElementById('youtube-results');
    
    let selectedTemplate = null;
    
    // Template selection
    templateItems.forEach(item => {
        item.addEventListener('click', function() {
            templateItems.forEach(t => t.classList.remove('selected'));
            this.classList.add('selected');
            selectedTemplate = this.dataset.template;
            
            // Update history section
            updateMemeHistory(selectedTemplate);
        });
    });
    
    generateBtn.addEventListener('click', async function() {
        if (!selectedTemplate) {
            alert('Please select a meme template');
            return;
        }
        
        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';
        
        try {
            const formData = new FormData();
            formData.append('template', selectedTemplate);
            formData.append('text', memeText.value);
            
            if (memeImage.files && memeImage.files[0]) {
                formData.append('image', memeImage.files[0]);
            }
            
            const response = await fetchAPI('/generate-meme', {
                method: 'POST',
                body: formData
            });
            
            generatedMeme.innerHTML = `
                <img src="${response.meme_url}" alt="Generated Meme">
                <div class="download-link">
                    <a href="${response.meme_url}" download target="_blank">Download</a>
                </div>
            `;
            
        } catch (error) {
            console.error('Meme generation error:', error);
            generatedMeme.innerHTML = 'Error: Could not generate meme.';
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Meme';
        }
    });
    
    // Add YouTube search functionality
    searchYoutubeBtn.addEventListener('click', async function() {
        if (!selectedTemplate || !memeText.value.trim()) {
            alert('Please select a template and add text to search for related videos');
            return;
        }
        
        searchYoutubeBtn.disabled = true;
        searchYoutubeBtn.textContent = 'Searching...';
        
        try {
            const query = memeText.value.split('|')[0]; // Use first text segment
            const era = getSelectedEra();
            
            const response = await fetch(`/search-youtube?query=${encodeURIComponent(query)}&era=${era}`);
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display YouTube results
            displayYouTubeResults(data.videos);
            
        } catch (error) {
            console.error('YouTube search error:', error);
            youtubeResults.innerHTML = `<p class="error">Error finding videos: ${error.message}</p>`;
        } finally {
            searchYoutubeBtn.disabled = false;
            searchYoutubeBtn.textContent = 'Find Related Videos';
        }
    });
    
    function displayYouTubeResults(videos) {
        if (!videos || videos.length === 0) {
            youtubeResults.innerHTML = '<p>No related videos found</p>';
            return;
        }
        
        youtubeResults.innerHTML = videos.map(video => `
            <div class="youtube-result">
                <h5>${video.title}</h5>
                <div class="youtube-embed">
                    <iframe 
                        width="100%" 
                        height="200" 
                        src="${video.embed_url}" 
                        title="${video.title}" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
                <p>Channel: ${video.channel}</p>
            </div>
        `).join('');
    }
    
    // Helper function to get the currently selected era
    function getSelectedEra() {
        const activeEraBtn = document.querySelector('.era-btn.active');
        return activeEraBtn ? activeEraBtn.dataset.era : '2020s';
    }
}

// Navigation between features
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.feature-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            
            // Update navigation
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Show target section
            sections.forEach(section => {
                section.classList.remove('active');
                
                if (section.id === targetId) {
                    section.classList.add('active');
                }
            });
        });
    });
}
