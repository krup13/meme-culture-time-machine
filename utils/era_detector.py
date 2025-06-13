import os
import re
import json
import openai
from dotenv import load_dotenv

class EraDetector:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Load slang dictionary for pattern matching
        with open('data/slang_dictionary.json', 'r') as f:
            self.slang_dictionary = json.load(f)
        
        # Era patterns for basic detection
        self.era_patterns = {
            "1990s": [
                r"dial-?up", r"aol", r"netscape", r"warez", r"y2k", r"napster",
                r"winamp", r"irc", r"l33t", r"pwned"
            ],
            "2000s": [
                r"myspace", r"xanga", r"friendster", r"limewire", r"bebo",
                r"lolcats", r"failblog", r"roflcopter", r"pwn", r"epic fail"
            ],
            "2010s": [
                r"yolo", r"swag", r"selfie", r"on fleek", r"bae", r"basic",
                r"literally", r"i can't even", r"netflix and chill", r"goals"
            ],
            "2020s": [
                r"sus", r"cap", r"no cap", r"simp", r"vibe check", r"poggers",
                r"cheugy", r"yeet", r"bussin", r"based"
            ]
        }
    
    def detect(self, content):
        """
        Detect what internet era the content is from
        """
        # Simple pattern-based detection first
        era_scores = self._pattern_detect(content)
        
        # If confidence is low, use AI
        top_era = max(era_scores, key=era_scores.get)
        confidence = era_scores[top_era]
        
        if confidence < 0.5:
            return self._ai_detect(content)
        
        return top_era
    
    def _pattern_detect(self, content):
        """Detect era based on pattern matching"""
        content = content.lower()
        scores = {"1990s": 0, "2000s": 0, "2010s": 0, "2020s": 0}
        
        # Check against regex patterns
        for era, patterns in self.era_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                scores[era] += len(matches) * 0.2  # Weight for exact matches
        
        # Check slang dictionary
        for era, slang_dict in self.slang_dictionary.items():
            for slang, meaning in slang_dict.items():
                if slang.lower() in content:
                    scores[era] += 0.1
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            for era in scores:
                scores[era] /= total
        
        return scores
    
    def _ai_detect(self, content):
        """Use AI to detect era based on content"""
        try:
            prompt = f"""
            Analyze the following text and determine which internet era it most likely belongs to:
            - 1990s (early internet, IRC, dial-up era)
            - 2000s (MySpace, early YouTube, pre-smartphone era)
            - 2010s (Facebook peak, Instagram rise, early TikTok)
            - 2020s (TikTok dominant, modern meme culture)
            
            Text to analyze: "{content}"
            
            Only respond with the era (1990s, 2000s, 2010s, or 2020s).
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an internet culture historian."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10
            )
            
            result = response.choices[0].message.content.strip()
            
            # Extract just the decade
            if "1990s" in result:
                return "1990s"
            elif "2000s" in result:
                return "2000s"
            elif "2010s" in result:
                return "2010s"
            elif "2020s" in result:
                return "2020s"
            else:
                # Default to 2020s if unrecognized
                return "2020s"
                
        except Exception as e:
            print(f"AI detection error: {str(e)}")
            # Fall back to most recent era if there's an error
            return "2020s"
