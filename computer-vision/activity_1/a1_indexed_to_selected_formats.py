import cv2
import numpy as np
import os

# Step 1: Create an indexed color image (palette-based 8-bit)
# We'll generate an image with a gradient using 256 colors
height, width = 256, 256
indexed_img = np.zeros((height, width), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        indexed_img[y, x] = (x + y) % 256  # Cycle through 0–255

# Step 2: Create a color palette (OpenCV doesn't store palettes directly, so we map them)
palette = np.array([[i, 255 - i, (i * 2) % 256] for i in range(256)], dtype=np.uint8)
indexed_color_img = cv2.applyColorMap(indexed_img, cv2.COLORMAP_JET)  # Simulated palette effect

# Step 3: Save in different formats
cv2.imwrite("indexed_output.jpg", indexed_color_img)
cv2.imwrite("indexed_output.png", indexed_color_img)
cv2.imwrite("indexed_output.bmp", indexed_color_img)

# Step 4: Check file sizes
for filename in ["indexed_output.jpg", "indexed_output.png", "indexed_output.bmp"]:
    size_bytes = os.path.getsize(filename)
    size_kb = size_bytes / 1024
    print(f"{filename}: {size_kb:.2f} KB")
