import os
import json
import openai
from dotenv import load_dotenv

class TextTranslator:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Load slang dictionary
        with open('data/slang_dictionary.json', 'r') as f:
            self.slang_dictionary = json.load(f)
    
    def translate(self, text, era):
        """
        Translate text to the specified internet era style
        """
        if era not in self.slang_dictionary:
            return f"Era {era} not supported"
            
        prompt = f"""
        Translate the following modern text into {era} internet language and slang:
        "{text}"
        
        Use these {era} slang terms as reference:
        {json.dumps(self.slang_dictionary[era])}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a {era} internet culture expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Translation error: {str(e)}"
