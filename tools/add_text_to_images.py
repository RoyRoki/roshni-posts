import os
import re
from PIL import Image, ImageDraw, ImageFont

# Configuration
POSTS_DIR = os.path.expanduser("/Users/test/Desktop/roshni/posts")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
# Fallback font if above doesn't exist
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

def parse_info_md(info_path):
    if not os.path.exists(info_path):
        return None, None
        
    with open(info_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    text_on_image = ""
    text_style = ""
    
    text_match = re.search(r'## Text on Image\n(.*?)(?=\n##|$)', content, re.DOTALL)
    if text_match:
        text_on_image = text_match.group(1).strip()
        
    style_match = re.search(r'## Text Style\n(.*?)(?=\n##|$)', content, re.DOTALL)
    if style_match:
        text_style = style_match.group(1).strip()
        
    return text_on_image, text_style

def get_drawing_params(style_text):
    style_lower = style_text.lower()
    fill = "white"
    stroke_fill = None
    stroke_width = 0
    
    colors = {
        "yellow": (255, 255, 0),
        "white": (255, 255, 255),
        "pink": (255, 192, 203),
        "blue": (0, 0, 255),
        "red": (255, 0, 0),
        "black": (0, 0, 0)
    }
    
    # Check for fill color
    for name, value in colors.items():
        if name in style_lower:
            fill = value
            break
            
    # Check for outline/stroke color
    if "outline" in style_lower or "shadow" in style_lower:
        stroke_width = 4
        parts = style_lower.split()
        for i, word in enumerate(parts):
            if word in ["outline", "shadow"] and i > 0:
                potential_color = parts[i-1]
                if potential_color in colors:
                    stroke_fill = colors[potential_color]
                    break
        # Fallback for outline color
        if not stroke_fill:
            if "blue" in style_lower: stroke_fill = colors["blue"]
            elif "pink" in style_lower: stroke_fill = colors["pink"]
            elif "red" in style_lower: stroke_fill = colors["red"]
            elif "black" in style_lower: stroke_fill = colors["black"]
            
    return fill, stroke_fill, stroke_width

def draw_text_on_image(image_path, text, style_text):
    if not os.path.exists(image_path) or not text:
        return
        
    try:
        img = Image.open(image_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Determine font size (approx 1/15th of height)
        font_size = int(height / 15)
        try:
            font = ImageFont.truetype(FONT_PATH, font_size)
        except:
            font = ImageFont.load_default()
            
        fill, stroke_fill, stroke_width = get_drawing_params(style_text)
        
        # Simple wrapping
        lines = text.split('\n')
        wrapped_lines = []
        max_chars = 25 # Guess for wrapping
        for line in lines:
            if len(line) > max_chars:
                # Basic wrap at spaces
                words = line.split()
                curr_line = ""
                for word in words:
                    if len(curr_line) + len(word) < max_chars:
                        curr_line += (word + " ")
                    else:
                        wrapped_lines.append(curr_line.strip())
                        curr_line = word + " "
                wrapped_lines.append(curr_line.strip())
            else:
                wrapped_lines.append(line)
        
        # Calculate total height of text block
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in wrapped_lines]
        total_text_height = sum(line_heights) + (len(wrapped_lines) - 1) * 10
        
        y = (height - total_text_height) // 2 # Center vertically
        
        for i, line in enumerate(wrapped_lines):
            # Center horizontally
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (width - line_width) // 2
            
            draw.text((x, y), line, font=font, fill=fill, 
                      stroke_width=stroke_width, stroke_fill=stroke_fill)
            y += line_heights[i] + 10
            
        final_img = img.convert("RGB")
        final_img.save(image_path)
        print(f"Successfully added text to {image_path}")
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main():
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
        
    post_folders = sorted(os.listdir(POSTS_DIR), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
    
    for folder in post_folders:
        folder_path = os.path.join(POSTS_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
            
        info_path = os.path.join(folder_path, "INFO.md")
        image_path = os.path.join(folder_path, "image.png")
        if not os.path.exists(image_path):
             # Try other extensions
             for ext in ['.jpg', '.jpeg', '.webp']:
                 p = os.path.join(folder_path, f"image{ext}")
                 if os.path.exists(p):
                     image_path = p
                     break
        
        if os.path.exists(info_path) and os.path.exists(image_path):
            print(f"Processing {folder}...")
            text, style = parse_info_md(info_path)
            if text:
                draw_text_on_image(image_path, text, style)

if __name__ == "__main__":
    main()
