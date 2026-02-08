import os
import shutil
import re

POSTS_DIR = "posts"
# The posts to remove
REMOVE_IDS = {3, 7, 15, 21, 31, 43, 49, 58}

def main():
    if not os.path.exists(POSTS_DIR):
        print(f"Directory {POSTS_DIR} does not exist.")
        return

    # 1. Remove the specified posts
    print(f"Removing posts: {sorted(list(REMOVE_IDS))}...")
    for pid in REMOVE_IDS:
        dir_path = os.path.join(POSTS_DIR, f"post{pid}")
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"Deleted {dir_path}")
            except Exception as e:
                print(f"Error deleting {dir_path}: {e}")
        else:
            print(f"Directory {dir_path} not found.")

    # 2. Renumber remaining posts
    # List all current post directories
    # Format: post1, post2, post4 ... (post3 is gone)
    
    # Get all items in posts dir
    items = os.listdir(POSTS_DIR)
    
    # Filter for post directories and extract numbers
    post_dirs = []
    for item in items:
        if item.startswith("post") and os.path.isdir(os.path.join(POSTS_DIR, item)):
            try:
                num = int(item[4:])
                post_dirs.append(num)
            except ValueError:
                pass
                
    post_dirs.sort()
    
    print(f"Remaining {len(post_dirs)} posts. Renumbering to 1-{len(post_dirs)}...")
    
    # Mapping: old_num -> new_num
    # We iterate sorted. 1 -> 1, 2 -> 2, 4 -> 3, 5 -> 4...
    
    # CAUTION: If we rename post4 to post3, and post3 was just deleted, it's fine.
    # But if we rename "post4" to "post3", we must ensure "post3" is free.
    # Since we deleted the targets first, "post3" IS free.
    # HOWEVER, if we have post4->post3, and then post5->post4.
    # If we iterate in increasing order:
    # Rename post4 -> post3. directory "post4" is gone.
    # Rename post5 -> post4. Works.
    # So iterating 1..N matches.
    
    new_count = 0
    
    for i, old_num in enumerate(post_dirs):
        new_num = i + 1
        
        if old_num == new_num:
            # Already correct
            # print(f"Post {old_num} stays as Post {new_num}")
            new_count += 1
            continue
            
        old_path = os.path.join(POSTS_DIR, f"post{old_num}")
        new_path = os.path.join(POSTS_DIR, f"post{new_num}")
        
        if os.path.exists(new_path):
            print(f"Conflict! {new_path} already exists. Skipping move of {old_num}.")
            # This shouldn't happen if we delete the gaps first and iterate sorted, 
            # unless there's a file named 'postX' that isn't in our list?
            # We already listed 'post_dirs' based on existence.
            # But wait, we just renamed something TO this?
            # Example: 1, 2, 4.
            # 1->1. 2->2. 4->3.
            # If 3 existed (it shouldn't, we deleted it), it would conflict.
            # We deleted 3. So 4->3 is safe.
            continue
            
        try:
            shutil.move(old_path, new_path)
            # print(f"Renamed post{old_num} -> post{new_num}")
            new_count += 1
        except Exception as e:
            print(f"Error renaming {old_path} to {new_path}: {e}")
            
    print(f"Renumbering complete. Total posts: {new_count}")

if __name__ == "__main__":
    main()
