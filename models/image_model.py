import os
import uuid
import base64
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
import requests
from io import BytesIO
from dotenv import load_dotenv

class ImageTransformer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("STABILITY_API_KEY")
        self.output_dir = "static/images/output/"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Era-specific parameters
        self.era_params = {
            "1990s": {
                "prompt": "1990s internet aesthetic, pixelated, low resolution, geometric patterns, Windows 95 style",
                "filter": "pixelate"
            },
            "2000s": {
                "prompt": "2000s MySpace aesthetic, heavy filters, Comic Sans font, clip art, glitter graphics",
                "filter": "sharpen"
            },
            "2010s": {
                "prompt": "Early 2010s Instagram vintage filters, motivational quotes, hipster style",
                "filter": "sepia"
            },
            "2020s": {
                "prompt": "Modern minimalist aesthetic, high contrast, clean lines",
                "filter": "enhance"
            }
        }
    
    def transform(self, image_file, era):
        """
        Transform an image to match the aesthetic of a specific internet era
        """
        if era not in self.era_params:
            return "Era not supported"
            
        # Save original image
        img = Image.open(image_file)
        
        # Apply era-specific filter
        img = self._apply_filter(img, era)
        
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(self.output_dir, filename)
        
        # Save transformed image
        img.save(output_path)
        
        # If Stability API is available, use it for more advanced transformation
        if self.api_key:
            try:
                img_base64 = self._get_base64_from_file(output_path)
                transformed_img = self._apply_stability_ai(img_base64, era)
                transformed_img.save(output_path)
            except Exception as e:
                print(f"Stability API error: {str(e)}")
        
        return f"/static/images/output/{filename}"
    
    def _apply_filter(self, img, era):
        """Apply basic filter based on era"""
        filter_type = self.era_params[era]["filter"]
        
        if filter_type == "pixelate":
            # Downsample then upsample for pixelation effect
            small_img = img.resize((img.width // 10, img.height // 10), resample=Image.NEAREST)
            img = small_img.resize(img.size, resample=Image.NEAREST)
            
        elif filter_type == "sharpen":
            # Add sharpening and saturation for 2000s look
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.5)
            
        elif filter_type == "sepia":
            # Apply sepia tone for 2010s Instagram look
            img = img.convert('RGB')
            w, h = img.size
            for i in range(w):
                for j in range(h):
                    r, g, b = img.getpixel((i, j))
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    img.putpixel((i, j), (tr if tr < 255 else 255, tg if tg < 255 else 255, tb if tb < 255 else 255))
                    
        elif filter_type == "enhance":
            # Enhance contrast and sharpness for modern look
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)
            
        return img
    
    def _get_base64_from_file(self, file_path):
        """Convert image file to base64 string"""
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    
    def _apply_stability_ai(self, img_base64, era):
        """Use Stability AI for image transformation"""
        prompt = self.era_params[era]["prompt"]
        
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            files={
                "init_image": img_base64
            },
            data={
                "text_prompts[0][text]": prompt,
                "text_prompts[0][weight]": 0.7,
                "init_image_mode": "image_strength",
                "image_strength": 0.35,
                "cfg_scale": 7,
                "samples": 1,
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            for i, image in enumerate(data["artifacts"]):
                img_data = base64.b64decode(image["base64"])
                return Image.open(BytesIO(img_data))
        else:
            raise Exception(f"API Error: {response.text}")
