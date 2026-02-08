import os
import time
import datetime
from tools.schedule_post import create_media_container, publish_media
from dotenv import load_dotenv

load_dotenv()

def local_schedule(image_url, caption, target_time_str):
    """
    target_time_str format: "YYYY-MM-DD HH:MM:SS"
    """
    try:
        target_dt = datetime.datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Error: Invalid time format. Use YYYY-MM-DD HH:MM:SS")
        return

    now = datetime.datetime.now()
    wait_seconds = (target_dt - now).total_seconds()

    if wait_seconds < 0:
        print(f"Error: Target time {target_time_str} is in the past!")
        return

    print(f"--- Local Scheduler ---")
    print(f"Target Time: {target_time_str}")
    print(f"Wait Time: {wait_seconds / 60:.2f} minutes")
    
    # 1. Create container now to verify inputs and get it ready
    container_id = create_media_container(image_url, caption)
    if not container_id:
        print("Failed to create media container. Aborting.")
        return

    print(f"\nSUCCESS: Media container created. Waiting for {wait_seconds / 60:.2f} minutes to publish...")
    
    # 2. Sleep until target time
    time.sleep(wait_seconds)
    
    # 3. Publish
    print(f"\nTime reached! Publishing now...")
    publish_media(container_id)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python tools/local_scheduler.py <image_url> <caption> <target_time>")
        print('Example: python tools/local_scheduler.py "url" "caption" "2026-02-09 01:45:00"')
    else:
        url = sys.argv[1]
        cap = sys.argv[2]
        target = sys.argv[3]
        local_schedule(url, cap, target)
