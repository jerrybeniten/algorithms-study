import cv2
import numpy as np
import os

# Get current directory where the program is running
current_dir = os.getcwd()

# Create a 1x1 true color (RGB) image - white pixel (255, 255, 255)
# dtype=uint8 for 8 bits per channel, 3 channels for RGB
pixelValue = [255, 255, 255]  # white
img = np.array([[pixelValue]], dtype=np.uint8)  # shape will be (1, 1, 3)

# Output path
out_path = os.path.join(current_dir, "C255_one_pixel_truecolor_opencv.bmp")

# Save as JPEG
cv2.imwrite(out_path, img)

print(f"Image saved at: {out_path}")
