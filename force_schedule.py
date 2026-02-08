from tools.schedule_post import schedule_media
import sys

# Container ID from last run
CONTAINER_ID = "17846006412684701"
TIMESTAMP = "1770580800"

if __name__ == "__main__":
    print(f"Force scheduling container {CONTAINER_ID} for {TIMESTAMP}...")
    schedule_media(CONTAINER_ID, TIMESTAMP)
