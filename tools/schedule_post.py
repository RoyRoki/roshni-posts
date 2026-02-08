import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")
API_VERSION = "v18.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def create_media_container(image_url, caption, scheduled_timestamp=None):
    """
    Creates a media container for an image.
    If scheduled_timestamp is provided, creates a scheduled container.
    """
    url = f"{BASE_URL}/{IG_USER_ID}/media"
    
    params = {
        "access_token": ACCESS_TOKEN,
        "image_url": image_url,
        "caption": caption
    }
    
    if scheduled_timestamp:
        params["scheduled_publish_time"] = scheduled_timestamp
        print(f"Creating SCHEDULED Media Container for {image_url} at {scheduled_timestamp}...")
    else:
        print(f"Creating Media Container for {image_url}...")
        
    try:
        response = requests.post(url, params=params)
        data = response.json()
        
        if "id" in data:
            container_id = data["id"]
            print(f"  -> Container ID: {container_id}")
            return container_id
        else:
            print(f"  -> Error: {data}")
            return None
    except Exception as e:
        print(f"  -> Request Failed: {e}")
        return None

def publish_media(container_id):
    """
    Publishes a media container (or confirms schedule).
    """
    url = f"{BASE_URL}/{IG_USER_ID}/media_publish"
    
    params = {
        "access_token": ACCESS_TOKEN,
        "creation_id": container_id
    }
    
    print(f"Publishing/Confirming Container {container_id}...")
    try:
        response = requests.post(url, params=params)
        data = response.json()
        
        if "id" in data:
            post_id = data["id"]
            print(f"  -> SUCCESS! Post/Schedule ID: {post_id}")
            return post_id
        else:
            print(f"  -> Error: {data}")
            return None
    except Exception as e:
        print(f"  -> Request Failed: {e}")
        return None

def main():
    if not ACCESS_TOKEN or not IG_USER_ID:
        print("Error: ACCESS_TOKEN or IG_USER_ID missing in .env")
        return

    print("--- Instagram Post Scheduler ---")
    image_url = input("Enter Public Image URL: ").strip()
    caption = input("Enter Caption: ").strip()
    
    if not image_url:
        print("Image URL is required.")
        return
        
    mode = input("Publish now (p) or Schedule (s)? ").strip().lower()
    timestamp = None
    
    if mode == 's':
        timestamp = input("Enter UNIX Timestamp for schedule: ").strip()
        if not timestamp:
            print("Timestamp required for scheduling.")
            return

    container_id = create_media_container(image_url, caption, scheduled_timestamp=timestamp)
    
    if container_id:
        if mode == 's':
            print("Confirming schedule...")
            publish_media(container_id)
        else:
            confirm = input("Publish now? (y/n): ").strip().lower()
            if confirm == 'y':
                publish_media(container_id)
            else:
                print("Skipped publishing.")

if __name__ == "__main__":
    main()
