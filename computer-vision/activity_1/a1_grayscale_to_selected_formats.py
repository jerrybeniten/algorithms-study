import cv2
import os

# Step 1: Load an image in grayscale mode
img = cv2.imread("input.jpg", 0)  # Ensure you have this image

# Step 2: Save in JPEG, PNG, and BMP formats
cv2.imwrite("output.jpg", img)
cv2.imwrite("output.png", img)
cv2.imwrite("output.bmp", img)

# Step 3: Check file sizes in bytes
for filename in ["output.jpg", "output.png", "output.bmp"]:
    size_bytes = os.path.getsize(filename)
    size_kb = size_bytes / 1024
    print(f"{filename}: {size_kb:.2f} KB")

"""
Expected outcome:
JPEG will usually be smallest because it’s lossy compression.
PNG will be larger than JPEG but smaller than BMP, because it uses lossless compression.
BMP will be largest because it’s basically raw pixel data without compression.
"""
