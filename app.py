from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from models.image_model import ImageTransformer
from models.voice_model import VoiceConverter
from models.meme_generator import MemeGenerator
from utils.era_detector import EraDetector
from utils.cringe_meter import CringeMeter
from services.google_services import GoogleVisionService, GoogleSpeechService, YouTubeService
from services.gemini_service import GeminiService
from models.text_model import TextTranslator

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize models
text_translator = TextTranslator()
image_transformer = ImageTransformer()
voice_converter = VoiceConverter()
meme_generator = MemeGenerator()
era_detector = EraDetector()
cringe_meter = CringeMeter()

# Initialize services
vision_service = GoogleVisionService()
speech_service = GoogleSpeechService()
youtube_service = YouTubeService()
gemini_service = GeminiService()  # Replace OpenAI with Gemini

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        # Get data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        text = data.get('text', '')
        era = data.get('era', '2000s')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        print(f"Received translation request - Text: '{text}', Era: {era}")
        
        # Use the actual TextTranslator instance
        translated = text_translator.translate(text, era)
        
        # Calculate mock cringe score
        import random
        cringe_score = random.randint(65, 95)
        
        response_data = {
            "translated": translated,
            "cringe_score": cringe_score,
            "original": text,
            "era": era
        }
        
        print(f"Translation successful: {translated[:30]}...")
        return jsonify(response_data)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in translate_text: {str(e)}")
        print(f"Error details: {error_details}")
        return jsonify({"error": "Server error: Could not translate text"}), 500

def mock_translate(text, era):
    """Provide reliable mock translations without external dependencies"""
    if era == "1990s":
        return f"<<< {text} >>> LOL!! *dials up modem sounds* ASL?? ~*~Only 90s kids will understand~*~ BRB, mom needs the phone line!!"
    elif era == "2000s":
        return f"~*~*{text}*~*~ roflmao!! xD :P (8) msn messenger status (8) brb g2g ttyl l8r sk8r"
    elif era == "2010s":
        return f"I can't even... {text} #blessed #nofilter #yolo #swag #tbt *insert instagram filter* literally dying rn"
    else:  # 2020s
        return f"no cap fr fr {text} 💀💅 *emotional damage* POV: you're reading this in 2023, vibing, it's giving main character energy"

@app.route('/transform-image', methods=['POST'])
def transform_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    era = request.form.get('era', '2000s')
    
    transformed_url = image_transformer.transform(image, era)
    return jsonify({'transformed_url': transformed_url})

@app.route('/convert-voice', methods=['POST'])
def convert_voice():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio provided'}), 400
    
    audio = request.files['audio']
    era = request.form.get('era', '2000s')
    
    converted_url = voice_converter.convert(audio, era)
    return jsonify({'converted_url': converted_url})

@app.route('/generate-meme', methods=['POST'])
def generate_meme():
    data = request.form
    template = data.get('template', 'drake')
    if 'image' in request.files:
        image = request.files['image']
    else:
        image = None
    text = data.get('text', '')
    
    meme_url = meme_generator.generate(template, image, text)
    return jsonify({'meme_url': meme_url})

@app.route('/detect-era', methods=['POST'])
def detect_era():
    data = request.json
    content = data.get('content', '')
    
    era = era_detector.detect(content)
    return jsonify({'era': era})

@app.route('/rate-cringe', methods=['POST'])
def rate_cringe():
    data = request.json
    if not data or 'content' not in data or 'era' not in data:
        return jsonify({'error': 'Missing content or era'}), 400
    
    content = data['content']
    era = data['era']
    
    try:
        # Replace OpenAI call with Gemini
        rating = gemini_service.rate_cringe(content, era)
        return jsonify({'rating': rating})
    except Exception as e:
        return jsonify({'error': f'Rating error: {str(e)}'}), 500

@app.route('/detect-image-era', methods=['POST'])
def detect_image_era():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    
    try:
        era = vision_service.detect_era(image)
        return jsonify({'era': era})
    except Exception as e:
        return jsonify({'error': f'Error detecting era: {str(e)}'}), 500

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    
    try:
        # Use Gemini Vision to analyze image
        analysis = gemini_service.analyze_image_context(image)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': f'Image analysis error: {str(e)}'}), 500

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio provided'}), 400
    
    audio = request.files['audio']
    
    try:
        transcript = speech_service.transcribe_audio(audio)
        return jsonify({'transcript': transcript})
    except Exception as e:
        return jsonify({'error': f'Error transcribing speech: {str(e)}'}), 500

@app.route('/search-youtube', methods=['GET'])
def search_youtube():
    query = request.args.get('query', '')
    era = request.args.get('era', None)
    max_results = int(request.args.get('max_results', 5))
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        videos = youtube_service.search_meme_videos(query, era, max_results)
        return jsonify({'videos': videos})
    except Exception as e:
        return jsonify({'error': f'Error searching YouTube: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
