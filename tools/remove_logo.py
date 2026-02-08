import cv2
import numpy as np
import os
import sys

# Configuration
POSTS_DIR = os.path.expanduser("/Users/test/Desktop/roshni/posts")

def remove_logo(image_path):
    print(f"Processing {image_path}...")
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read {image_path}")
        return False
        
    h, w = img.shape[:2]
    
    # Define the region of interest (ROI) for the logo
    # The user said "right bottom". Let's assume a 60x60 square at the bottom right.
    # We might need to adjust this based on the specific logo size.
    # Based on typical watermarks, let's start with 80x80 pixels from the corner.
    offset_x = 80
    offset_y = 80
    
    # Coordinates of the top-left corner of the rectangle to inpaint
    x1 = w - offset_x
    y1 = h - offset_y
    x2 = w
    y2 = h
    
    # Create a mask
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # Mask the bottom right corner
    # cv2.rectangle(img, pt1, pt2, color, thickness)
    # We set the mask to 255 (white) in the area we want to inpaint
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
    
    # Inpaint
    # radius 3, using TELEA algorithm
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    # Overwrite the original image
    cv2.imwrite(image_path, dst)
    print(f"Successfully processed {image_path}")
    return True

def main():
    if len(sys.argv) > 1:
        # Process specific file(s)
        for arg in sys.argv[1:]:
            remove_logo(arg)
    else:
        # Process all images in posts/post*/image.png
        count = 0
        if not os.path.exists(POSTS_DIR):
             print(f"Directory {POSTS_DIR} does not exist.")
             return

        for root, dirs, files in os.walk(POSTS_DIR):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in {'.png', '.jpg', '.jpeg', '.webp'}: # Add support for other formats
                    full_path = os.path.join(root, file)
                    if remove_logo(full_path):
                        count += 1
        print(f"Finished processing {count} images.")

if __name__ == "__main__":
    main()
