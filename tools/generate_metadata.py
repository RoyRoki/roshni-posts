import os
import re

DATA_FILE = os.path.expanduser("/Users/test/Desktop/roshni/tools/posts_data.txt")
POSTS_DIR = os.path.expanduser("/Users/test/Desktop/roshni/posts")

def parse_posts(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    post_pattern = re.compile(r'(?:^|\n)(.{0,5}POST\s+(\d+)\s+[^\n]*)', re.IGNORECASE)
    
    matches = list(post_pattern.finditer(content))
    
    posts = []
    
    for i, match in enumerate(matches):
        start_idx = match.start()
        post_num = int(match.group(2))
        header_line = match.group(1).strip()
        
        if i < len(matches) - 1:
            end_idx = matches[i+1].start()
            post_content = content[start_idx:end_idx]
        else:
            post_content = content[start_idx:]
            
        posts.append({
            'num': post_num,
            'header': header_line,
            'content': post_content
        })
        
    return posts

def extract_section(content, section_name):
    if section_name == 'PROMPT':
        pattern = re.compile(r'(?:🖼️\s*IMAGE(?: GENERATION)? PROMPT)(.*?)(?=(?:Text on image:|Text style:|📝|🔖|$))', re.DOTALL | re.IGNORECASE)
    elif section_name == 'TEXT_ON_IMAGE':
        pattern = re.compile(r'(?:Text on image:)(.*?)(?=(?:Text style:|📝|🔖|$))', re.DOTALL | re.IGNORECASE)
    elif section_name == 'TEXT_STYLE':
        pattern = re.compile(r'(?:Text style:)(.*?)(?=(?:📝|🔖|$))', re.DOTALL | re.IGNORECASE)
    elif section_name == 'CAPTION':
        pattern = re.compile(r'(?:📝\s*CAPTION)(.*?)(?=(?:🔖|$))', re.DOTALL | re.IGNORECASE)
    elif section_name == 'HASHTAGS':
        pattern = re.compile(r'(?:🔖\s*HASHTAGS)(.*?)(?=$)', re.DOTALL | re.IGNORECASE)
    else:
        return ""

    match = pattern.search(content)
    if match:
        return match.group(1).strip()
    return ""

def write_info_file(target_dir, md_content):
    if not os.path.exists(target_dir):
        print(f"Warning: Directory {target_dir} does not exist. Skipping.")
        return

    target_file = os.path.join(target_dir, "INFO.md")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Generated {target_file}")

def generate_files():
    if not os.path.exists(DATA_FILE):
        print(f"Data file not found: {DATA_FILE}")
        return

    posts_data = parse_posts(DATA_FILE)
    print(f"Found {len(posts_data)} posts in data file.")
    
    # We have 68 Text Posts (indexed 0 to 67 in list, or Post 1 to Post 68)
    # Target Folders: post1 to post68
    
    # User Request Logic:
    # "post68 info is for post67 image" -> Text 68 goes to Post 67.
    # Implies a shift: Post N gets Text N+1.
    # We will wrap Text 1 to Post 68 to complete the cycle.
    
    # Map Folder Number (1-68) to Text Index (0-67)
    # Text Index = (Folder Num) % 68
    # Examples:
    # Folder 1 -> Text Index 1 (Text Post 2)
    # Folder 2 -> Text Index 2 (Text Post 3)
    # ...
    # Folder 67 -> Text Index 67 (Text Post 68)
    # Folder 68 -> Text Index 0 (Text Post 1)
    
    # Updated Mapping Logic: 1:1 Mapping
    # User Request: "68 is good" (Text 68), "67 is 66" (Error).
    # Implication: User wants Post N -> Text N for ALL posts.
    
    total_posts = len(posts_data)
    for folder_num in range(1, total_posts + 1):
        # Calculate text index (0-based)
        text_idx = folder_num - 1
            
        post = posts_data[text_idx]
        
        # Extract Data
        prompt = extract_section(post['content'], 'PROMPT')
        text_on_image = extract_section(post['content'], 'TEXT_ON_IMAGE')
        text_style = extract_section(post['content'], 'TEXT_STYLE')
        caption = extract_section(post['content'], 'CAPTION')
        hashtags = extract_section(post['content'], 'HASHTAGS')
        
        text_on_image = text_on_image.strip('"')

        md_content = f"""# Post {folder_num} Data (Source Text {post['num']})

## Image Prompt
{prompt}

## Text on Image
{text_on_image}

## Text Style
{text_style}

## Caption
{caption}

## Hashtags
{hashtags}
"""
        
        target_dir = os.path.join(POSTS_DIR, f"post{folder_num}")
        write_info_file(target_dir, md_content)

if __name__ == "__main__":
    generate_files()
