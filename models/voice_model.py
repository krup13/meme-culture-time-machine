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
        
        self.dependencies_met = self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if all required dependencies are available."""
        try:
            import speech_recognition as sr
            from google.cloud import speech, texttospeech
            
            # Check Google Cloud credentials
            if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
                print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set")
                return False
                
            return True
        except ImportError as e:
            print(f"Missing dependency: {e}")
            return False
    
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
    
    def record_audio(self, duration=5):
        """Record audio from microphone."""
        if not self.dependencies_met:
            return {"error": "Voice dependencies not installed. Run setup_voice_converter.py first."}
            
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Recording... Speak now!")
                audio_data = recognizer.record(source, duration=duration)
                
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with open(temp_file.name, "wb") as f:
                f.write(audio_data.get_wav_data())
                
            return {"success": True, "file_path": temp_file.name}
        except Exception as e:
            print(f"Error recording audio: {e}")
            return {"error": f"Could not record audio: {str(e)}"}
    
    def convert_to_era(self, audio_file, era):
        """Convert voice to match the specified era."""
        if not self.dependencies_met:
            return {"error": "Voice dependencies not installed. Run setup_voice_converter.py first."}
            
        try:
            # 1. Convert speech to text
            text = self._speech_to_text(audio_file)
            if not text:
                return {"error": "Could not transcribe audio"}
                
            # 2. Modify text to match era style using text translator
            from models.text_model import TextTranslator
            translator = TextTranslator()
            era_text = translator.translate_to_era(text, era)
            
            # 3. Convert modified text back to speech with era-specific voice
            output_file = self._text_to_speech(era_text, era)
            
            return {
                "success": True,
                "original_text": text,
                "era_text": era_text,
                "audio_file": output_file
            }
        except Exception as e:
            print(f"Error in voice conversion: {e}")
            return {"error": f"Voice conversion failed: {str(e)}"}
    
    def _speech_to_text(self, audio_file):
        """Convert speech to text using Google Cloud Speech."""
        try:
            from google.cloud import speech
            
            client = speech.SpeechClient()
            
            with open(audio_file, "rb") as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=44100,
                language_code="en-US",
            )
            
            response = client.recognize(config=config, audio=audio)
            
            # Get text from response
            text = ""
            for result in response.results:
                text += result.alternatives[0].transcript
                
            return text
        except Exception as e:
            print(f"Speech to text error: {e}")
            return None
    
    def _text_to_speech(self, text, era):
        """Convert text to speech with era-specific voice settings."""
        try:
            from google.cloud import texttospeech
            
            client = texttospeech.TextToSpeechClient()
            
            # Configure voice based on era
            voice_params = self._get_era_voice_params(era)
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name=voice_params["voice_name"]
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                effects_profile_id=["medium-bluetooth-speaker-class-device"],
                pitch=voice_params["pitch"],
                speaking_rate=voice_params["rate"]
            )
            
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            # Save output to a temp file
            output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
                
            # Apply audio effects based on era
            self._apply_era_audio_effects(output_file, era)
                
            return output_file
        except Exception as e:
            print(f"Text to speech error: {e}")
            return None
    
    def _get_era_voice_params(self, era):
        """Get voice parameters based on era."""
        params = {
            "1990s": {
                "voice_name": "en-US-Wavenet-F",
                "pitch": -2.0,  # Lower pitch for that 90s computer voice feel
                "rate": 0.85    # Slightly slower for dial-up era
            },
            "2000s": {
                "voice_name": "en-US-Wavenet-D",
                "pitch": 0.0,   # Standard pitch
                "rate": 1.0     # Standard rate
            },
            "2010s": {
                "voice_name": "en-US-Wavenet-C",
                "pitch": 2.0,   # Higher pitch for younger/upspeak
                "rate": 1.1     # Slightly faster
            },
            "2020s": {
                "voice_name": "en-US-Wavenet-H",
                "pitch": 0.5,   # Modern natural voice
                "rate": 1.15    # Slightly fast-paced for TikTok era
            }
        }
        return params.get(era, params["2000s"])
    
    def _apply_era_audio_effects(self, audio_file, era):
        """Apply era-specific audio effects."""
        try:
            audio = AudioSegment.from_file(audio_file)
            
            if era == "1990s":
                # Low quality, phone-like filter
                audio = audio.set_channels(1)  # Mono
                audio = audio.set_frame_rate(8000)  # Low sample rate
                # Add static noise
                from pydub.generators import WhiteNoise
                noise = WhiteNoise().to_audio_segment(duration=len(audio)) - 25
                audio = audio.overlay(noise)
                
            elif era == "2000s":
                # Slightly compressed, like early digital
                audio = audio.compress_dynamic_range()
                
            elif era == "2010s":
                # More processed, clearer but with subtle effects
                audio = audio.high_pass_filter(800)
                audio = audio.low_pass_filter(4000)
                
            # 2020s - keep high quality with no effects
                
            # Export back to the file
            audio.export(audio_file, format="mp3")
            
        except Exception as e:
            print(f"Could not apply audio effects: {e}")
