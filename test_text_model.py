#!/usr/bin/env python3
"""
Test script for the updated TextTranslator model
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.text_model import TextTranslator

def test_text_translator():
    """Test the TextTranslator with mock translations"""
    print("Testing TextTranslator with mock translation fallback...")
    print("=" * 60)
    
    # Initialize the translator
    translator = TextTranslator()
    
    # Test text
    test_text = "Hello everyone, how are you doing today?"
    
    # Test different eras
    eras = ["1990s", "2000s", "2010s", "2020s"]
    
    for era in eras:
        print(f"\nTesting {era} translation:")
        print(f"Original: {test_text}")
        try:
            translated = translator.translate(test_text, era)
            print(f"Translated: {translated}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test unsupported era
    print(f"\nTesting unsupported era:")
    try:
        result = translator.translate(test_text, "1980s")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_text_translator()
