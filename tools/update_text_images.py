import os
import re
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Configuration
POSTS_DIR = "posts"
# Use a standard English font or load a specific one
# DejaVuSans.ttf is often available, or Arial.
# On macOS, Helvetica or Arial is good.
FONT_PATH_ENGLISH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH_ENGLISH):
    FONT_PATH_ENGLISH = "/System/Library/Fonts/Helvetica.ttc"

FONT_SIZE = 60
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
SHADOW_OFFSET = 2

# List of posts to process (Bangla transliteration posts)
TARGET_POSTS = {"post3", "post7", "post15", "post21", "post31", "post43", "post49", "post58"}

def get_text_on_image(info_path):
    try:
        with open(info_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = re.search(r"## Text on Image\s*\n(.*?)\n##", content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            return text
    except Exception as e:
        print(f"Error reading {info_path}: {e}")
    return None

def clear_bottom_area(image_path):
    """
    Attempts to clear the bottom text area using inpainting.
    Assumes text is at the bottom center.
    """
    print(f"  Clearing old text from {image_path}...")
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to read {image_path}")
        return False
        
    h, w = img.shape[:2]
    
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # Define rectangle: start 400px from bottom (approx)
    y_start = h - 400 
    if y_start < 0: y_start = 0
    
    # Margin from sides
    x_margin = 20
    
    # Create mask for the bottom area
    cv2.rectangle(mask, (x_margin, y_start), (w - x_margin, h - 20), 255, -1)
    
    # Inpaint
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    cv2.imwrite(image_path, dst)
    return True

def add_text_to_image(image_path, text):
    try:
        # First clear old text
        if not clear_bottom_area(image_path):
            return False

        # Re-open the image (now modified by cv2)
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(FONT_PATH_ENGLISH, FONT_SIZE)
        except Exception:
            print(f"Warning: Could not load {FONT_PATH_ENGLISH}, trying default.")
            font = ImageFont.load_default()

        # Calculate text position (Centered horizontally, Bottom with margin)
        lines = text.split('\n')
        
        img_w, img_h = img.size
        
        # Calculate total text height
        total_text_h = 0
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h + 10) 
            total_text_h += h + 10
            
        current_y = img_h - total_text_h - 100 
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            x = (img_w - text_w) / 2
            
            # Draw shadow
            draw.text((x + SHADOW_OFFSET, current_y + SHADOW_OFFSET), line, font=font, fill=SHADOW_COLOR)
            # Draw text
            draw.text((x, current_y), line, font=font, fill=TEXT_COLOR)
            
            current_y += line_heights[i]
            
        img.save(image_path)
        print(f"  Added new text to {image_path}")
        return True
        
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
        return False

def main():
    if not os.path.exists(POSTS_DIR):
        print(f"Directory {POSTS_DIR} does not exist.")
        return

    count = 0
    
    for subdir in TARGET_POSTS:
        dir_path = os.path.join(POSTS_DIR, subdir)
        info_path = os.path.join(dir_path, "INFO.md")
        image_path = os.path.join(dir_path, "image.png")
        
        if os.path.exists(info_path) and os.path.exists(image_path):
            text = get_text_on_image(info_path)
            
            if text:
                print(f"Processing {subdir} with text: {text}")
                if add_text_to_image(image_path, text):
                    count += 1
                
    print(f"Finished. Updated {count} images.")

if __name__ == "__main__":
    main()
