from tools.schedule_post import publish_media
import sys

# Container ID from last run
CONTAINER_ID = "17846005629684701"

if __name__ == "__main__":
    print(f"Force publishing container {CONTAINER_ID}...")
    publish_media(CONTAINER_ID)
