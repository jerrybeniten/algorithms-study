import os
import cv2
import numpy as np

# Get directory where the current Python file is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Step 1: Create a 1-pixel RGB image (pure red)
rgb_pixel = np.array([[[0, 0, 255]]], dtype=np.uint8)  # OpenCV uses BGR, so red is (0,0,255)

# Save original red pixel TIFF
rgb_path = os.path.join(script_dir, 'one_pixel_red_rgb.tiff')
cv2.imwrite(rgb_path, rgb_pixel)

# Step 2: Convert RGB to grayscale using OpenCV
gray_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_BGR2GRAY)

# Save grayscale pixel TIFF
gray_path = os.path.join(script_dir, 'one_pixel_red_grayscale.tiff')
cv2.imwrite(gray_path, gray_pixel)

print("RGB TIFF saved at:", rgb_path)
print("Grayscale TIFF saved at:", gray_path)
