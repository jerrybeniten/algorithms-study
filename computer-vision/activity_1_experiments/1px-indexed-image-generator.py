import cv2
import numpy as np
import os

# Current directory
current_dir = os.getcwd()

# Step 1: Create a 1x1 indexed color image (value = index in palette)
# We'll use index 1 for white
indexed_img = np.array([[1]], dtype=np.uint8)

# Step 2: Create a color palette
# index 0 = black, index 1 = white
palette = np.zeros((256, 3), dtype=np.uint8)
palette[0] = [0, 0, 0]        # black
palette[1] = [255, 255, 255]  # white

# Step 3: Map indexed image to RGB
rgb_img = palette[indexed_img]

# Step 4: Save as JPEG
out_path = os.path.join(current_dir, "C255_one_pixel_indexed_opencv.png")
cv2.imwrite(out_path, rgb_img)
