import os
import json
import sys
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.schedule_post import create_media_container, publish_media

# Load environment variables
load_dotenv()

# Configuration
POSTS_DIR = Path("posts")
STATE_FILE = Path("tools/post_state.json")
BASE_URL = os.getenv("BASE_URL")

def load_state():
    if not STATE_FILE.exists():
        print(f"State file {STATE_FILE} not found. Creating with default.")
        return {"next_post_id": 1}
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading state: {e}")
        return {"next_post_id": 1}

def save_state(state):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"State updated: next_post_id is now {state['next_post_id']}")
    except Exception as e:
        print(f"Error saving state: {e}")

def get_post_info(post_id):
    post_dir = POSTS_DIR / f"post{post_id}"
    info_path = post_dir / "INFO.md"
    image_path = post_dir / "image.png"

    if not info_path.exists() or not image_path.exists():
        print(f"Post {post_id} files missing (checked {info_path} and {image_path})")
        return None

    # Read caption from INFO.md
    # We'll extract the text under "## Caption" and "## Hashtags"
    try:
        with open(info_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        caption_match = content.split("## Caption")
        hashtags_match = content.split("## Hashtags")
        
        caption_text = ""
        hashtags_text = ""
        
        if len(caption_match) > 1:
            # Take expected caption section, stop at next header if any (likely Hashtags)
            temp = caption_match[1].split("##")[0].strip()
            caption_text = temp
            
        if len(hashtags_match) > 1:
            temp = hashtags_match[1].strip()
            hashtags_text = temp
            
        full_caption = f"{caption_text}\n.\n.\n{hashtags_text}"
        return full_caption.strip()
        
    except Exception as e:
        print(f"Error reading info for post {post_id}: {e}")
        return None

def main():
    print(f"--- Daily Poster Run: {datetime.datetime.now()} ---")
    
    if not BASE_URL:
        print("Error: BASE_URL not found in .env. Cannot construct image URL.")
        return

    state = load_state()
    current_id = state.get("next_post_id", 1)
    
    print(f"Attempting to publish Post {current_id}...")
    
    caption = get_post_info(current_id)
    if not caption:
        print(f"Skipping Post {current_id}: Content not found or incomplete.")
        # Optional: Increment to try next one, or stop? 
        # For now, let's stop to avoid skipping a valid but slightly malformed post without fixing.
        # But if folder is missing entirely, maybe we should stop.
        return

    # Construct Image URL
    # Assumes BASE_URL points to the root of the repo/hosting
    # e.g. https://xyz.ngrok.io/posts/post1/image.png
    image_url = f"{BASE_URL}/posts/post{current_id}/image.png"
    
    print(f"Image URL: {image_url}")
    print(f"Caption: {caption[:50]}...")

    # 1. Create Container
    container_id = create_media_container(image_url, caption)
    
    if container_id:
        # 2. Publish
        publish_id = publish_media(container_id)
        
        if publish_id:
            print(f"Successfully published Post {current_id}!")
            # 3. Update State
            state["next_post_id"] = current_id + 1
            save_state(state)
        else:
            print("Failed to publish media container.")
    else:
        print("Failed to create media container.")

if __name__ == "__main__":
    main()
