import time
import sys
import random

def simulate_process():
    total_images = 100
    print("Starting watermark removal process...")
    print("-" * 50)

    for i in range(1, total_images + 1):
        # Simulate processing time (random between 0.05s and 0.15s)
        time.sleep(random.uniform(0.05, 0.15))
        
        # Calculate percentage
        percent = (i / total_images) * 100
        
        # Create progress bar
        bar_length = 30
        filled_length = int(bar_length * i // total_images)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # Print status line (overwrite previous line if supported, but for simple scroll effect we print new lines)
        # The user asked for "dummy show", scrolling might be better for video to show activity.
        # "semulate the terminal commond" -> usually means seeing lines scroll by.
        
        print(f"\rPost {i}/{total_images}: [posts/post{i}/image.png] Removing watermark... Done", end="")
        sys.stdout.flush()
        
        # Print a newline every now and then or just let it overwrite?
        # If I want it to look like processing a list of files, I should print new lines.
        # "100/100 complete water mark removed"
        # Let's do a scrolling log style, it looks more "hacker/terminal" for video.
        print(f"\r[INFO] Processing posts/post{i}/image.png ... Success")
        
        # Update specific progress bar at the bottom? 
        # Simpler: Just print the file processing line.
    
    print("-" * 50)
    print(f"✅ Successfully processed {total_images}/{total_images} images.")
    print("All watermarks have been removed.")

if __name__ == "__main__":
    try:
        simulate_process()
    except KeyboardInterrupt:
        print("\nProcess interrupted.")
