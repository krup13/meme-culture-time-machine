# MemeLord Chronos - Meme Culture Time Machine

A web application that translates content across different internet eras and meme cultures.

## Features

- **Era Translator**: Convert modern text into different internet era styles
- **Aesthetic Time Warp**: Transform photos to match different era aesthetics
- **Voice Era Converter**: Convert speech to match different era "vibes"
- **Meme Format Generator**: Generate content in classic meme formats
- **Era Detector**: AI guesses what era content is from
- **Cringe Meter**: Rates how authentically "cringe" your retro content is

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   STABILITY_API_KEY=your_stability_api_key
   ```
4. Create necessary directories:
   ```
   mkdir -p static/images/output
   mkdir -p static/images/memes
   mkdir -p static/audio/output
   ```
5. Run the application:
   ```
   flask run
   ```
6. Open your browser and navigate to `http://localhost:5000`

## Technology Stack

- **Backend**: Python Flask
- **AI APIs**: OpenAI, ElevenLabs, Stability AI
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

- `app.py`: Main Flask application
- `models/`: AI model implementations
- `utils/`: Utility functions
- `templates/`: HTML templates
- `static/`: Static assets (CSS, JS, images)
- `data/`: JSON data files

## Demo

The application allows users to:
1. Translate text between internet eras (1990s-2020s)
2. Transform images to match era-specific aesthetics
3. Convert voice recordings to match era-specific speech patterns
4. Generate classic meme formats with user content

Each feature also has a UI that adapts to the selected era for an immersive experience.