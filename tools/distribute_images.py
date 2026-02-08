import os
import shutil
import time
from datetime import datetime, timedelta

# Configuration
DOWNLOADS_DIR = os.path.join(os.getcwd(), "test") # Use 'test' directory in CWD
POSTS_DIR = "posts"
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}

def distribute_images():
    # 1. Find all images in the source directory
    candidates = []
    
    print(f"Scanning {DOWNLOADS_DIR} for images...")
    
    try:
        if not os.path.exists(DOWNLOADS_DIR):
             print(f"Source directory {DOWNLOADS_DIR} does not exist.")
             return

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
                
            # Get modification time
            mtime = os.path.getmtime(filepath)
            candidates.append((filepath, mtime))
            
    except Exception as e:
        print(f"Error scanning source dir: {e}")
        return

    # 2. Sort candidates by modification time (oldest first)
    # User requested "short on timestam" (sort on timestamp)
    candidates.sort(key=lambda x: x[1])

    if not candidates:
        print("No images found.")
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
    # Adjust POSTS_DIR if running from tools/
    if not os.path.exists(POSTS_DIR):
        if os.path.exists(os.path.join("..", POSTS_DIR)):
             POSTS_DIR = os.path.join("..", POSTS_DIR)
             # If we are in tools/, then test/ is likely in .. / test
             if os.path.basename(current_cwd) == "tools":
                 DOWNLOADS_DIR = os.path.join("..", "test")
        elif os.path.exists(os.path.join(current_cwd, "posts")):
             POSTS_DIR = os.path.join(current_cwd, "posts")
    
    distribute_images()
