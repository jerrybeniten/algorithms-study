import cv2
import numpy as np
import os

# Step 1: Create or load a binary image (black & white only)
# Here I create a sample 256x256 binary image with a simple pattern
binary_img = np.zeros((256, 256), dtype=np.uint8)
binary_img[::2, ::2] = 255  # Checkerboard pattern
binary_img[1::2, 1::2] = 255

# Step 2: Save binary image in different formats
cv2.imwrite("output.jpg", binary_img)
cv2.imwrite("output.png", binary_img)
cv2.imwrite("output.bmp", binary_img)

# Step 3: Check file sizes
for filename in ["output.jpg", "output.png", "output.bmp"]:
    size_bytes = os.path.getsize(filename)
    size_kb = size_bytes / 1024
    print(f"{filename}: {size_kb:.2f} KB")
