import os
import io
import json
from dotenv import load_dotenv
from google.cloud import vision, speech
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load environment variables
load_dotenv()

class GoogleVisionService:
    """Service for Google Cloud Vision API integration"""
    
    def __init__(self):
        # Initialize Vision client
        # Note: This assumes you have GOOGLE_APPLICATION_CREDENTIALS set in your environment
        # or you have a credentials.json file
        self.client = vision.ImageAnnotatorClient()
    
    def analyze_image(self, image_file):
        """Analyze image content using Google Vision API"""
        # Read the image file
        content = image_file.read()
        image = vision.Image(content=content)
        
        # Feature types to request
        features = [
            vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
            vision.Feature(type_=vision.Feature.Type.WEB_DETECTION),
            vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES)
        ]
        
        # Perform API request
        response = self.client.annotate_image({
            'image': image,
            'features': features
        })
        
        return {
            'labels': [label.description for label in response.label_annotations],
            'web_entities': [entity.description for entity in response.web_detection.web_entities],
            'colors': [
                {
                    'color': f'rgb({int(color.color.red)}, {int(color.color.green)}, {int(color.color.blue)})',
                    'score': color.score,
                    'pixel_fraction': color.pixel_fraction
                }
                for color in response.image_properties_annotation.dominant_colors.colors
            ]
        }
    
    def detect_era(self, image_file):
        """Try to estimate the era of the image based on content and styling"""
        analysis = self.analyze_image(image_file)
        
        # Reset the file pointer for future use
        image_file.seek(0)
        
        # Era indicators
        era_keywords = {
            "1990s": ["90s", "1990s", "dial-up", "windows 95", "floppy disk", "vhs", "y2k"],
            "2000s": ["2000s", "myspace", "flash", "early internet", "web 1.0", "pixel art"],
            "2010s": ["2010s", "instagram", "meme", "facebook", "social media", "smartphone"],
            "2020s": ["tiktok", "modern", "minimalist", "clean", "high-res", "4k"]
        }
        
        # Calculate scores for each era based on matching keywords
        era_scores = {era: 0 for era in era_keywords}
        
        # Check labels and web entities for era keywords
        all_texts = analysis['labels'] + analysis['web_entities']
        for text in all_texts:
            text_lower = text.lower()
            for era, keywords in era_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    era_scores[era] += 1
        
        # Check colors for era association
        colors = analysis['colors']
        
        # 90s had bright neon colors
        neon_count = sum(1 for color in colors if self._is_neon(color['color']))
        if neon_count >= 2:
            era_scores["1990s"] += 2
        
        # 2000s often had dark backgrounds with bright accents
        dark_count = sum(1 for color in colors if self._is_dark(color['color']))
        if dark_count >= 2:
            era_scores["2000s"] += 1
        
        # 2010s often had vintage filters (faded colors)
        faded_count = sum(1 for color in colors if self._is_faded(color['color']))
        if faded_count >= 2:
            era_scores["2010s"] += 1
        
        # 2020s often has minimal color palettes with high contrast
        minimal_palette = len(colors) <= 3
        if minimal_palette:
            era_scores["2020s"] += 1
        
        # Return the era with highest score or the most recent if tie
        max_score = max(era_scores.values())
        if max_score == 0:
            return "2020s"  # Default to most recent
        
        # Get all eras with the max score
        top_eras = [era for era, score in era_scores.items() if score == max_score]
        # Return the most recent era among those with the highest score
        for era in ["2020s", "2010s", "2000s", "1990s"]:
            if era in top_eras:
                return era
    
    def _is_neon(self, rgb_str):
        """Check if a color is neon (very bright and saturated)"""
        # Extract RGB values
        rgb = rgb_str.replace('rgb(', '').replace(')', '').split(', ')
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        
        # Neon colors have high brightness and saturation
        brightness = (r + g + b) / 3
        max_channel = max(r, g, b)
        min_channel = min(r, g, b)
        saturation = (max_channel - min_channel) / max_channel if max_channel > 0 else 0
        
        return brightness > 180 and saturation > 0.5
    
    def _is_dark(self, rgb_str):
        """Check if a color is dark"""
        rgb = rgb_str.replace('rgb(', '').replace(')', '').split(', ')
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        brightness = (r + g + b) / 3
        return brightness < 80
    
    def _is_faded(self, rgb_str):
        """Check if a color has the faded/vintage look"""
        rgb = rgb_str.replace('rgb(', '').replace(')', '').split(', ')
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        
        # Faded/vintage typically has reduced saturation but not too dark/light
        max_channel = max(r, g, b)
        min_channel = min(r, g, b)
        saturation = (max_channel - min_channel) / max_channel if max_channel > 0 else 0
        brightness = (r + g + b) / 3
        
        return saturation < 0.3 and 80 < brightness < 200


class GoogleSpeechService:
    """Service for Google Cloud Speech-to-Text API integration"""
    
    def __init__(self):
        # Initialize Speech client
        self.client = speech.SpeechClient()
    
    def transcribe_audio(self, audio_file, language_code="en-US"):
        """Transcribe speech to text using Google Speech-to-Text API"""
        # Read audio file
        content = audio_file.read()
        
        # Configure the request
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True
        )
        
        # Perform the transcription
        response = self.client.recognize(config=config, audio=audio)
        
        # Extract the transcript
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript
        
        return transcript


class YouTubeService:
    """Service for YouTube Data API integration"""
    
    def __init__(self):
        # Get API key from environment
        self.api_key = os.getenv("GOOGLE_YOUTUBE_API_KEY")
        
        # Initialize YouTube API client
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_meme_videos(self, query, era=None, max_results=5):
        """Search YouTube for meme videos relevant to query and era"""
        # Add era to query if specified
        full_query = query
        if era:
            full_query = f"{query} {era} meme"
        else:
            full_query = f"{query} meme"
        
        # Execute search
        search_response = self.youtube.search().list(
            q=full_query,
            part='snippet',
            maxResults=max_results,
            type='video'
        ).execute()
        
        # Process results
        videos = []
        for item in search_response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail = item['snippet']['thumbnails']['high']['url']
            channel = item['snippet']['channelTitle']
            
            videos.append({
                'id': video_id,
                'title': title,
                'thumbnail': thumbnail,
                'channel': channel,
                'embed_url': f"https://www.youtube.com/embed/{video_id}"
            })
        
        return videos
