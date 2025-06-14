import os
import json
from dotenv import load_dotenv

class TextTranslator:
    def __init__(self):
        load_dotenv()
        self.api_available = False
        self.model = None
        
        # Try to import Google Generative AI module and set up API
        try:
            import google.generativeai as genai
            self.genai = genai
            
            # Check if GEMINI_API_KEY is set (try both possible names)
            api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_GEMINI_API_KEY')
            if not api_key:
                print("Warning: GEMINI_API_KEY not set. Using mock translation.")
                self.api_available = False
            else:
                try:
                    self.genai.configure(api_key=api_key)
                    # Test the API key by creating a model (using current model name)
                    self.model = self.genai.GenerativeModel('gemini-1.5-flash')
                    self.api_available = True
                    print("Gemini API initialized successfully.")
                except Exception as e:
                    print(f"Warning: Failed to initialize Gemini API: {str(e)}. Using mock translation.")
                    self.api_available = False
                
        except ImportError as e:
            print(f"Warning: Google Generative AI module not available: {str(e)}. Using mock translation.")
            self.api_available = False

        # Load slang dictionary with error handling
        try:
            with open('data/slang_dictionary.json', 'r') as f:
                self.slang_dictionary = json.load(f)
        except FileNotFoundError:
            print("Warning: slang_dictionary.json not found. Using default dictionary.")
            self.slang_dictionary = {
                "1990s": {"lol": "laugh out loud", "asl": "age/sex/location"},
                "2000s": {"rofl": "rolling on floor laughing", "brb": "be right back"},
                "2010s": {"yolo": "you only live once", "swag": "style"},
                "2020s": {"no cap": "no lie", "fr": "for real"}
            }

    def translate(self, text, era):
        """
        Translate text to the specified internet era style
        Falls back to mock translation if API is unavailable or fails
        """
        # Validate era
        if era not in self.slang_dictionary:
            return f"Era {era} not supported. Available eras: {list(self.slang_dictionary.keys())}"
        
        # If API is not available, use mock translation
        if not self.api_available:
            print(f"API not available. Using mock translation for era: {era}")
            return self._mock_translation(text, era)
            
        try:
            # Create a prompt based on the era
            prompt = self._create_prompt(text, era)
            
            print(f"Attempting Gemini API translation for era: {era}")
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            # Extract translated text
            if response and hasattr(response, 'text') and response.text:
                print(f"Gemini API translation successful for era: {era}")
                return response.text.strip()
            else:
                print("Empty or invalid response from Gemini API")
                return self._mock_translation(text, era)
                
        except Exception as e:
            print(f"Gemini API error: {str(e)}. Falling back to mock translation.")
            # Fallback to mock translation
            return self._mock_translation(text, era)
    
    def _create_prompt(self, text, era):
        """
        Create a prompt for the Gemini API based on the era
        """
        slang_terms = self.slang_dictionary.get(era, {})
        return f"""
        Translate the following modern text into {era} internet language and slang:
        "{text}"
        
        Use these {era} slang terms and style as reference:
        {json.dumps(slang_terms, indent=2)}
        
        Make it sound authentic to the {era} internet culture while keeping the original meaning.
        """
    
    def _mock_translation(self, text, era):
        """Provide direct era translations without analytical text."""
        if era == "1990s":
            # 90s internet style
            text_upper = text.upper() if len(text) < 15 else text
            emoticons = [":)", ":P", ":-)", ">:)", ":-D", ";)"]
            ascii_art = ["(^_^)", "<(^.^)>", "\\(^o^)/", "(>_<)", "(o_O)", "(*_*)"]
            
            import random
            result = f">>> {text_upper} <<<\n"
            result += f"**COOL DUDE** {random.choice(emoticons)} {random.choice(ascii_art)}\n"
            result += f"omg did u just say that?? LOL!! *dials up modem*\n"
            result += f"a/s/l?? gotta go my mom needs 2 use the phone!!\n"
            
            # Replace modern terms
            result = result.replace("cool", "rad").replace("internet", "information superhighway")
            return result
        
        elif era == "2000s":
            # MySpace/MSN era
            dec = "~*~*~" * (len(text) // 20 + 1)
            emoticons = ["xD", ":P", "^_^", "o.O", "<3", "=^_^=", ":3"]
            
            import random
            result = f"{dec}\n"
            result += f"{text} roflmao!! {random.choice(emoticons)}\n"
            result += f"(8) my msn messenger status (8)\n"
            result += f"brb g2g ttyl!! {dec}"
            return result
        
        elif era == "2010s":
            # Tumblr/Instagram
            import random
            hashtags = ["#blessed", "#nofilter", "#yolo", "#swag", "#tbt", "#instagood", "#likeforlike", "#followme"]
            selected_tags = random.sample(hashtags, min(4, len(hashtags)))
            
            result = f"I can't even...\n\n{text}\n\n"
            result += "✨ " + " ✨ ".join(selected_tags) + " ✨\n"
            result += f"*insert instagram filter*\n"
            result += f"omg literally dying rn 😂"
            return result
        
        else:  # 2020s
            # TikTok/modern
            import random
            phrases = ["no cap fr fr", "it's giving", "main character energy", "rent free", "living for this"]
            emojis = ["💀", "✨", "👁️👄👁️", "💅", "🔥", "🤌", "🥺"]
            
            result = f"{random.choice(phrases)} {text}\n"
            result += f"{' '.join(random.sample(emojis, min(3, len(emojis))))}\n"
            result += f"POV: you're reading this in {random.randint(2020, 2025)}"
            return result
