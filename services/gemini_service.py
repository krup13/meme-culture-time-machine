import os
import base64
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

class GeminiService:
    """Service for Google Gemini AI integration"""
    
    def __init__(self):
        # Get API key from environment
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY environment variable not set")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize models
        self.text_model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
    
    def translate_text_to_era(self, text, era):
        """Translate modern text to a specific internet era style"""
        prompt = f"""
        Transform the following text to match the internet and meme culture style of the {era} era.
        Maintain the original meaning but change the vocabulary, tone, and style to match how people
        would have expressed themselves online during the {era}.
        
        Original text: {text}
        
        Respond with ONLY the transformed text, nothing else.
        """
        
        response = self.text_model.generate_content(prompt)
        return response.text.strip()
    
    def rate_cringe(self, content, era):
        """Rate how authentically 'cringe' content is for a specific era"""
        prompt = f"""
        Rate how authentically "cringe" or era-appropriate the following content would be for the {era} internet culture.
        Consider aspects like vocabulary, references, formatting, and style.
        Give a rating from 1-10, where 10 is extremely authentic to the {era} internet culture.
        
        Content: {content}
        
        Respond with ONLY a number from 1 to 10, nothing else.
        """
        
        response = self.text_model.generate_content(prompt)
        try:
            rating = float(response.text.strip())
            # Ensure rating is between 1 and 10
            return max(1, min(10, rating))
        except ValueError:
            # Default to middle rating if we can't parse the response
            return 5.0
    
    def analyze_image_context(self, image_file):
        """Analyze the context of an image using Gemini Vision"""
        # Read image file
        image_bytes = image_file.read()
        image_file.seek(0)  # Reset file pointer for future use
        
        # Create image object for Gemini
        image = Image.open(io.BytesIO(image_bytes))
        
        # Prompt for image analysis
        prompt = """
        Analyze this image and provide:
        1. A brief description of what's in the image
        2. Any memes or internet culture references you can identify
        3. The approximate era it might be from (1990s, 2000s, 2010s, or 2020s)
        4. Key visual elements and style
        
        Format your response as JSON with these fields:
        {
            "description": "brief description",
            "meme_references": ["reference1", "reference2"],
            "likely_era": "era",
            "visual_elements": ["element1", "element2"]
        }
        """
        
        response = self.vision_model.generate_content([prompt, image])
        
        # Process response
        # Note: Ideally we'd parse JSON but for robustness, we'll extract key fields
        text_response = response.text
        
        # If response looks like JSON, try to clean it up
        if '{' in text_response and '}' in text_response:
            import json
            import re
            
            # Extract JSON part using regex
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', text_response, re.DOTALL)
            if not json_match:
                json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
            
            if json_match:
                try:
                    json_str = json_match.group(1) if json_match.groups() else json_match.group(0)
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass  # Fall back to text parsing
        
        # Fall back to simple parsing
        return {
            "description": extract_section(text_response, "description", "brief description"),
            "meme_references": extract_list(text_response, "meme_references"),
            "likely_era": extract_section(text_response, "likely_era", "2020s"),
            "visual_elements": extract_list(text_response, "visual_elements")
        }
    
    def generate_meme_text(self, template, input_text, era=None):
        """Generate appropriate text for a meme template"""
        era_context = f"in the style of {era} internet culture" if era else "that's funny"
        
        prompt = f"""
        Create text for a {template} meme template {era_context}.
        Use this input as inspiration: {input_text}
        
        For this template, provide the text in the exact format needed with sections separated by '|' characters.
        Respond with ONLY the meme text, nothing else.
        """
        
        response = self.text_model.generate_content(prompt)
        return response.text.strip()
    
    def detect_content_era(self, content):
        """Detect which internet era (1990s, 2000s, 2010s, 2020s) content is from"""
        prompt = f"""
        Analyze this content and determine which internet era it most likely belongs to.
        Choose from: 1990s, 2000s, 2010s, or 2020s.
        
        Content: {content}
        
        Consider vocabulary, references, formatting, and style.
        Respond with ONLY the era (1990s, 2000s, 2010s, or 2020s), nothing else.
        """
        
        response = self.text_model.generate_content(prompt)
        era = response.text.strip().lower()
        
        # Ensure valid era is returned
        valid_eras = ["1990s", "2000s", "2010s", "2020s"]
        for valid_era in valid_eras:
            if valid_era.lower() in era:
                return valid_era
        
        # Default if no valid era detected
        return "2020s"


# Helper functions for response parsing
def extract_section(text, section_name, default=""):
    """Extract a section from text based on section name"""
    import re
    
    # Try to find the section using various patterns
    patterns = [
        rf'"{section_name}"\s*:\s*"([^"]*)"',  # "section": "value"
        rf'"{section_name}"\s*:\s*\'([^\']*)\'',  # "section": 'value'
        rf'{section_name}:\s*(.*?)(?:,|\n|$)',  # section: value
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return default

def extract_list(text, section_name):
    """Extract a list section from text"""
    import re
    
    # Try to find the section using various patterns
    list_match = re.search(rf'"{section_name}"\s*:\s*\[(.*?)\]', text, re.DOTALL)
    
    if list_match:
        items_text = list_match.group(1)
        # Extract quoted strings
        items = re.findall(r'"([^"]*)"', items_text)
        if items:
            return items
    
    # If not found or empty, try to extract based on formatting
    if section_name.lower() in text.lower():
        section_text = text.split(section_name, 1)[1]
        lines = section_text.split("\n")
        items = []
        for line in lines[:5]:  # Look at first 5 lines after section name
            if line.strip().startswith("- "):
                items.append(line.strip()[2:])
        if items:
            return items
    
    return []
