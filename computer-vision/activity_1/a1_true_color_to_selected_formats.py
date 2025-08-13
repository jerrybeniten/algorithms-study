import cv2
import numpy as np
import os

# Create a true color image (200x200 RGB)
truecolor_img = np.zeros((200, 200, 3), dtype=np.uint8)
truecolor_img[:, :100] = [255, 0, 0]   # Blue
truecolor_img[:, 100:] = [0, 255, 0]   # Green

cv2.imwrite("truecolor.jpg", truecolor_img)
cv2.imwrite("truecolor.png", truecolor_img)
cv2.imwrite("truecolor.bmp", truecolor_img)

print("\nTrue color image sizes:")
for filename in ["truecolor.jpg", "truecolor.png", "truecolor.bmp"]:
    size_kb = os.path.getsize(filename) / 1024
    print(f"{filename}: {size_kb:.2f} KB")
