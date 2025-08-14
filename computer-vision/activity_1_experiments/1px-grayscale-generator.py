import cv2
import numpy as np
import os

# Get current directory where the program is running
current_dir = os.getcwd()

# Create a 1x1 grayscale image with pixel value 128
pixelValue = 255
img = np.array([[pixelValue]], dtype=np.uint8)

# Output path in the current directory
out_path = os.path.join(current_dir, "C" + str(pixelValue) + "_one_pixel_gray_opencv.webp")

# Save the image
cv2.imwrite(out_path, img)

print(f"Image saved at: {out_path}")
