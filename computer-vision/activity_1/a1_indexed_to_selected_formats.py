import cv2
import numpy as np
import os

# Simulated indexed color (palette of 4 colors)
indexed_img = np.zeros((200, 200), dtype=np.uint8)
indexed_img[:100, :100] = 50    # gray
indexed_img[100:, :100] = 100   # lighter gray
indexed_img[:100, 100:] = 150   # darker gray
indexed_img[100:, 100:] = 200   # even darker gray

cv2.imwrite("indexed.jpg", indexed_img)
cv2.imwrite("indexed.png", indexed_img)
cv2.imwrite("indexed.bmp", indexed_img)

print("\nIndexed color image sizes:")
for filename in ["indexed.jpg", "indexed.png", "indexed.bmp"]:
    size_kb = os.path.getsize(filename) / 1024
    print(f"{filename}: {size_kb:.2f} KB")
