import os
import json
import uuid
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import requests
import io
import base64

class MemeGenerator:
    def __init__(self):
        load_dotenv()
        self.output_dir = "static/images/memes/"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Load meme templates
        with open('data/meme_templates.json', 'r') as f:
            self.templates = json.load(f)
    
    def generate(self, template_name, image=None, text=""):
        """
        Generate a meme using the specified template, image, and text
        """
        if template_name not in self.templates:
            return "Template not found"
        
        template = self.templates[template_name]
        
        # Create the meme based on template type
        if template["type"] == "text_only":
            return self._create_text_meme(template, text)
        elif template["type"] == "image_text":
            if not image:
                return "Image required for this template"
            return self._create_image_text_meme(template, image, text)
        elif template["type"] == "multi_panel":
            if not image:
                return "Image required for this template"
            return self._create_multi_panel_meme(template, image, text)
        else:
            return "Unknown template type"
    
    def _create_text_meme(self, template, text):
        """Create a text-only meme"""
        # Load template background
        bg_path = os.path.join("static/images/templates", template["background"])
        img = Image.open(bg_path)
        
        draw = ImageDraw.Draw(img)
        
        # Split text if there are multiple text fields
        text_parts = text.split('|')
        
        for i, text_field in enumerate(template["text_fields"]):
            if i < len(text_parts):
                field_text = text_parts[i]
                position = tuple(text_field["position"])
                font_size = text_field.get("font_size", 36)
                font_color = text_field.get("color", "white")
                
                # Load font
                font = ImageFont.truetype("static/fonts/impact.ttf", font_size)
                
                # Add text to image
                draw.text(position, field_text, font=font, fill=font_color, stroke_width=2, stroke_fill="black")
        
        # Save the meme
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(self.output_dir, filename)
        img.save(output_path)
        
        return f"/static/images/memes/{filename}"
    
    def _create_image_text_meme(self, template, image, text):
        """Create a meme with user image and text"""
        # Load template background
        bg_path = os.path.join("static/images/templates", template["background"])
        base_img = Image.open(bg_path)
        
        # Open and resize user image to fit in the template
        user_img = Image.open(image)
        
        for img_field in template["image_fields"]:
            width = img_field["width"]
            height = img_field["height"]
            position = tuple(img_field["position"])
            
            # Resize user image
            resized_user_img = user_img.resize((width, height))
            
            # Paste user image onto template
            base_img.paste(resized_user_img, position)
        
        draw = ImageDraw.Draw(base_img)
        
        # Split text if there are multiple text fields
        text_parts = text.split('|')
        
        for i, text_field in enumerate(template["text_fields"]):
            if i < len(text_parts):
                field_text = text_parts[i]
                position = tuple(text_field["position"])
                font_size = text_field.get("font_size", 36)
                font_color = text_field.get("color", "white")
                
                # Load font
                font = ImageFont.truetype("static/fonts/impact.ttf", font_size)
                
                # Add text to image
                draw.text(position, field_text, font=font, fill=font_color, stroke_width=2, stroke_fill="black")
        
        # Save the meme
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(self.output_dir, filename)
        base_img.save(output_path)
        
        return f"/static/images/memes/{filename}"
    
    def _create_multi_panel_meme(self, template, image, text):
        """Create a multi-panel meme (like Drake format)"""
        # Load template
        bg_path = os.path.join("static/images/templates", template["background"])
        base_img = Image.open(bg_path)
        
        # Open user image
        user_img = Image.open(image)
        
        # If there's panel image placement, use it
        if "panels" in template:
            for panel in template["panels"]:
                panel_img = user_img.copy()
                width = panel["width"]
                height = panel["height"]
                position = tuple(panel["position"])
                
                # Apply transformations if specified
                if "rotate" in panel:
                    panel_img = panel_img.rotate(panel["rotate"], expand=True)
                if "flip" in panel and panel["flip"]:
                    panel_img = panel_img.transpose(Image.FLIP_LEFT_RIGHT)
                
                # Resize user image for this panel
                resized_panel_img = panel_img.resize((width, height))
                
                # Paste into template
                base_img.paste(resized_panel_img, position)
        
        draw = ImageDraw.Draw(base_img)
        
        # Add text to panels if specified
        text_parts = text.split('|')
        
        for i, text_field in enumerate(template["text_fields"]):
            if i < len(text_parts):
                field_text = text_parts[i]
                position = tuple(text_field["position"])
                font_size = text_field.get("font_size", 36)
                font_color = text_field.get("color", "white")
                
                # Load font
                font = ImageFont.truetype("static/fonts/impact.ttf", font_size)
                
                # Add text to image
                draw.text(position, field_text, font=font, fill=font_color, stroke_width=2, stroke_fill="black")
        
        # Save the meme
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(self.output_dir, filename)
        base_img.save(output_path)
        
        return f"/static/images/memes/{filename}"
