import os
import re
import json
import openai
from dotenv import load_dotenv

class CringeMeter:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Load slang dictionary
        with open('data/slang_dictionary.json', 'r') as f:
            self.slang_dictionary = json.load(f)
        
        # Cringe indicators by era
        self.cringe_indicators = {
            "1990s": [
                (r"leet\s*speak", 2),
                (r"asl\?", 1.5),
                (r"<marquee>", 3),
                (r"under construction", 2),
                (r"cyber", 1.5)
            ],
            "2000s": [
                (r"rawr\s*xD", 3),
                (r"(\(\:|\:D|\:P)", 1),  # Emoticons
                (r"epic\s*fail", 2),
                (r"o\s*rly", 2.5),
                (r"(\\m/|rock\s*on)", 1.5)
            ],
            "2010s": [
                (r"(hash)?yolo", 2.5),
                (r"(hash)?swag", 2),
                (r"epic\s*win", 1.5),
                (r"keep\s*calm\s*and", 3),
                (r"like\s*a\s*boss", 2)
            ],
            "2020s": [
                (r"no\s*cap", 1),
                (r"(sus|sussy)", 2),
                (r"(vibe\s*check|pass\s*the\s*vibe\s*check)", 1.5),
                (r"not\s*me\s*.{1,15}", 1.5),  # "not me doing X"
                (r"(sheesh|sksksk|and\s*i\s*oop)", 2)
            ]
        }
    
    def rate(self, content, era):
        """
        Rate how authentically "cringe" the content is for the specified era
        Returns a score from 1-10
        """
        content = content.lower()
        base_score = 5  # Default middle score
        
        # Simple pattern-based cringe detection
        pattern_score = self._pattern_rate(content, era)
        
        # Use AI for more nuanced analysis if available
        ai_score = self._ai_rate(content, era)
        
        # Combine scores (weighting AI higher if available)
        if ai_score > 0:
            final_score = (pattern_score + (ai_score * 2)) / 3
        else:
            final_score = pattern_score
        
        # Ensure score is between 1-10
        return max(1, min(10, round(final_score)))
    
    def _pattern_rate(self, content, era):
        """Rate cringe based on pattern matching"""
        score = 5  # Start with neutral score
        
        if era not in self.cringe_indicators:
            return score
        
        # Check against regex patterns for specified era
        for pattern, weight in self.cringe_indicators[era]:
            matches = re.findall(pattern, content, re.IGNORECASE)
            score += len(matches) * weight * 0.5
        
        # Check slang usage
        if era in self.slang_dictionary:
            era_slang = self.slang_dictionary[era]
            for slang in era_slang:
                if slang.lower() in content:
                    score += 0.5
        
        # Look for over-usage indicators
        exclamation_count = content.count('!')
        if exclamation_count > 3:
            score += min(2, exclamation_count * 0.2)
        
        # ALL CAPS sections
        caps_matches = re.findall(r'\b[A-Z]{3,}\b', content)
        score += len(caps_matches) * 0.3
        
        # Repeated letters (like "soooooo")
        repeated_chars = re.findall(r'(\w)\1{3,}', content)
        score += len(repeated_chars) * 0.4
        
        # Cap the pattern score
        return max(1, min(10, score))
    
    def _ai_rate(self, content, era):
        """Use AI to rate cringe factor"""
        try:
            era_descriptions = {
                "1990s": "early internet slang, 'leet speak', dial-up references, ASCII art",
                "2000s": "MySpace emo culture, random XD, excessive emoticons, early memes",
                "2010s": "YOLO, hashtag overuse, 'epic' everything, Keep Calm memes",
                "2020s": "TikTok slang, 'no cap', 'sus', stan culture language"
            }
            
            prompt = f"""
            Rate how authentically "cringey" this content is for {era} internet culture.
            Example {era} internet culture includes: {era_descriptions.get(era, "")}
            
            Content: "{content}"
            
            Provide a rating from 1-10 where:
            1 = not cringey at all for the era
            5 = moderately cringey
            10 = extremely, authentically cringey for {era}
            
            Only respond with a number from 1-10.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an internet culture historian specializing in cringe culture."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10
            )
            
            result = response.choices[0].message.content.strip()
            
            # Extract just the number
            match = re.search(r'(\d+)', result)
            if match:
                return int(match.group(1))
            else:
                return 0
                
        except Exception as e:
            print(f"AI cringe rating error: {str(e)}")
            return 0  # Return 0 to indicate AI rating failed
