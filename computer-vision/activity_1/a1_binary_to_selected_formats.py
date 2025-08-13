import cv2
import numpy as np
import os

# Create a binary image (black/white)
binary_img = np.zeros((200, 200), dtype=np.uint8)
binary_img[50:150, 50:150] = 255  # white square

cv2.imwrite("binary.jpg", binary_img)
cv2.imwrite("binary.png", binary_img)
cv2.imwrite("binary.bmp", binary_img)

print("Binary image sizes:")
for filename in ["binary.jpg", "binary.png", "binary.bmp"]:
    size_kb = os.path.getsize(filename) / 1024
    print(f"{filename}: {size_kb:.2f} KB")

"""
Binary image sizes:
binary.jpg: 1.89 KB
binary.png: 0.68 KB
binary.bmp: 40.12 KB
"""