import cv2
import os
from matlab import im2uint8

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load a .tiff image
img = cv2.imread("one_pixel_red_grayscale.tiff", cv2.IMREAD_UNCHANGED)  # Keep original bit depth

# Convert to uint8 using our custom function
gray_uint8 = im2uint8(img)

processed_path = os.path.join(script_dir, 'one_pixel_red_grayscale_uint8.tiff')
cv2.imwrite(processed_path, gray_uint8)

# Show results
cv2.imshow("Original", img)
cv2.imshow("After im2uint8", gray_uint8)
cv2.waitKey(0)
cv2.destroyAllWindows()
