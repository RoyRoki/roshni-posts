import os
import shutil
import time
from datetime import datetime, timedelta

# Configuration
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
POSTS_DIR = "posts"
TIME_WINDOW_HOURS = 1
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}

def distribute_images():
    # 1. Find images in Downloads modified in the last hour
    now = datetime.now()
    cutoff_time = now - timedelta(hours=TIME_WINDOW_HOURS)
    
    candidates = []
    
    print(f"Scanning {DOWNLOADS_DIR} for images modified after {cutoff_time}...")
    
    try:
        for filename in os.listdir(DOWNLOADS_DIR):
            if filename.startswith('.'):
                continue
                
            filepath = os.path.join(DOWNLOADS_DIR, filename)
            
            # Check if it's a file
            if not os.path.isfile(filepath):
                continue
                
            # Check extension
            ext = os.path.splitext(filename)[1].lower()
            if ext not in IMAGE_EXTENSIONS:
                continue
                
            # Check modification time
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime >= cutoff_time:
                candidates.append((filepath, mtime))
    except Exception as e:
        print(f"Error scanning Downloads: {e}")
        return

    # 2. Sort candidates by modification time (oldest first? or newest? usually newest downloaded is last modified)
    # The user said "first downloaded image of last 1h" -> "next image go post2"
    # This implies sorting by time. "First downloaded" usually means oldest in the window? 
    # Or order of download? 
    # Let's assume sorting by mtime ascending (oldest to newest) matches "first downloaded".
    candidates.sort(key=lambda x: x[1])

    if not candidates:
        print("No matching images found in the last hour.")
        return

    print(f"Found {len(candidates)} images to distribute.")

    # 3. Distribute to posts/postX/image.png
    for i, (source_path, mtime) in enumerate(candidates):
        post_num = i + 1
        target_dir = os.path.join(POSTS_DIR, f"post{post_num}")
        target_file = os.path.join(target_dir, "image.png")
        
        # Ensure target directory exists
        os.makedirs(target_dir, exist_ok=True)
        
        try:
            print(f"Moving {source_path} -> {target_file}")
            shutil.move(source_path, target_file)
        except Exception as e:
            print(f"Failed to move {source_path} to {target_file}: {e}")

if __name__ == "__main__":
    current_cwd = os.getcwd()
    if not os.path.exists(POSTS_DIR):
        # Fallback if running from tools/ or similar
        # Try to find posts dir relative to script or cwd
        if os.path.exists(os.path.join("..", POSTS_DIR)):
             POSTS_DIR = os.path.join("..", POSTS_DIR)
        elif os.path.exists(os.path.join(current_cwd, "posts")):
             POSTS_DIR = os.path.join(current_cwd, "posts")
        else:
             print(f"Could not find {POSTS_DIR} directory.")
             exit(1)
             
    distribute_images()
