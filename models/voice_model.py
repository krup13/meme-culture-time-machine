import os
import uuid
import requests
from pydub import AudioSegment
import tempfile
from dotenv import load_dotenv

class VoiceConverter:
    def __init__(self):
        load_dotenv()
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.output_dir = "static/audio/output/"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Era-specific voice styles
        self.era_voices = {
            "1990s": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",  # Example voice ID for robotic voice
                "settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            },
            "2000s": {
                "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Example voice ID for valley girl
                "settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.8,
                    "style": 0.3,
                    "use_speaker_boost": True
                }
            },
            "2010s": {
                "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Example voice ID for millennial vocal fry
                "settings": {
                    "stability": 0.8,
                    "similarity_boost": 0.8,
                    "style": 0.6,
                    "use_speaker_boost": True
                }
            },
            "2020s": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Example voice ID for modern voice
                "settings": {
                    "stability": 0.9,
                    "similarity_boost": 0.7,
                    "style": 0.4,
                    "use_speaker_boost": True
                }
            }
        }
    
    def convert(self, audio_file, era):
        """
        Convert audio to match the specified internet era voice style
        """
        if era not in self.era_voices:
            return "Era not supported"
        
        # Convert the uploaded audio to text
        audio_text = self._speech_to_text(audio_file)
        
        # Generate era-specific voice from text
        output_filename = self._text_to_speech(audio_text, era)
        
        return output_filename
    
    def _speech_to_text(self, audio_file):
        """Convert speech to text"""
        # Save audio to temp file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
            audio = AudioSegment.from_file(audio_file)
            audio.export(temp_audio_path, format="mp3")
        
        # Use OpenAI's Whisper API or another STT service
        try:
            audio_file = open(temp_audio_path, "rb")
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
                files={"file": audio_file},
                data={"model": "whisper-1"}
            )
            
            if response.status_code == 200:
                text = response.json().get("text", "")
                return text
            else:
                return "Sorry, could not transcribe audio."
                
        except Exception as e:
            return f"Speech to text error: {str(e)}"
        finally:
            # Clean up temp file
            os.remove(temp_audio_path)
    
    def _text_to_speech(self, text, era):
        """Convert text to speech with era-specific voice"""
        if not text:
            return "No text to convert"
            
        voice_id = self.era_voices[era]["voice_id"]
        settings = self.era_voices[era]["settings"]
        
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": settings
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                # Generate unique filename
                filename = f"{uuid.uuid4()}.mp3"
                output_path = os.path.join(self.output_dir, filename)
                
                # Save audio file
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                return f"/static/audio/output/{filename}"
            else:
                print(f"ElevenLabs API error: {response.status_code}, {response.text}")
                return "Error generating speech"
                
        except Exception as e:
            print(f"Text to speech error: {str(e)}")
            return "Error generating speech"
