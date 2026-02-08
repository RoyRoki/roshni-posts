import os
import shutil
import datetime
import re

# Configuration
SOURCE_DIR = os.path.expanduser("~/Downloads")
DEST_BASE_DIR = os.path.expanduser("/Users/test/Desktop/roshni/posts")
# We use today's date to filter downloads
TODAY_DATE = datetime.date.today()

def is_today(timestamp):
    dt = datetime.date.fromtimestamp(timestamp)
    return dt == TODAY_DATE

def get_next_post_number(base_dir):
    """
    Scans the base_dir for folders named 'postN' and returns the next available number.
    Returns 1 if no 'postN' folders are found.
    """
    if not os.path.exists(base_dir):
        return 1
        
    max_num = 0
    pattern = re.compile(r'^post(\d+)$')
    
    try:
        for entry in os.scandir(base_dir):
            if entry.is_dir():
                match = pattern.match(entry.name)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num
    except OSError as e:
        print(f"Error scanning destination directory: {e}")
        return 1
        
    return max_num + 1

def get_todays_images(source_dir):
    """
    Returns a list of file entries from source_dir that are images and modified today.
    Sorted by modification time (oldest first).
    """
    images = []
    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return []

    entries = []
    try:
        entries = list(os.scandir(source_dir))
    except (PermissionError, OSError) as e:
        print(f"Error accessing {source_dir}: {e}")
        return []

    for entry in entries:
        if not entry.is_file():
            continue
            
        if entry.name.startswith('.'):
            continue

        ext = os.path.splitext(entry.name)[1].lower()
        if ext not in valid_extensions:
            continue
            
        try:
            mtime = entry.stat().st_mtime
            if is_today(mtime):
                images.append(entry)
        except OSError:
            continue
            
    # Sort by modification time (oldest first)
    images.sort(key=lambda x: x.stat().st_mtime)
    return images

def organize_images():
    print(f"Checking for images from today ({TODAY_DATE})...")
    images = get_todays_images(SOURCE_DIR)
    
    if not images:
        print("No new images found for today in Downloads.")
        return

    print(f"Found {len(images)} images to organize.")
    
    # Ensure destination base directory exists
    os.makedirs(DEST_BASE_DIR, exist_ok=True)
    
    # Get the next starting number
    start_num = get_next_post_number(DEST_BASE_DIR)
    print(f"Starting at post{start_num}")
    
    for i, image_entry in enumerate(images):
        current_num = start_num + i
        post_dir_name = f"post{current_num}"
        dest_dir = os.path.join(DEST_BASE_DIR, post_dir_name)
        
        os.makedirs(dest_dir, exist_ok=True)
        
        ext = os.path.splitext(image_entry.name)[1].lower()
        
        # Consistent naming strategy
        target_filename = "image.png"
        if ext != '.png':
             target_filename = f"image{ext}"
        
        dest_path = os.path.join(dest_dir, target_filename)
        
        print(f"Moving {image_entry.name} -> {post_dir_name}/{target_filename}")
        try:
            shutil.move(image_entry.path, dest_path)
        except Exception as e:
            print(f"Error moving {image_entry.name}: {e}")

if __name__ == "__main__":
    organize_images()
