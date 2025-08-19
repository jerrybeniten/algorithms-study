import cv2
import numpy as np
import os

# Current directory
current_dir = os.getcwd()

# Create a 1x1 true binary white pixel in memory
binary_img = np.array([[True]], dtype=bool)

# Convert to 8-bit for OpenCV (255 white, 0 black)
pixelValue = 255
img_for_jpeg = (binary_img.astype(np.uint8)) * 255

# Save as JPEG
out_path = os.path.join(current_dir, "C" + str(pixelValue) + "_one_pixel_binary_opencv.bmp")
cv2.imwrite(out_path, img_for_jpeg)

print(f"Image saved at: {out_path}")