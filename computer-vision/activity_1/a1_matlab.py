import cv2
from matlab import im2uint8

# Load a .tiff image
img = cv2.imread("example.tiff", cv2.IMREAD_UNCHANGED)  # Keep original bit depth

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert to uint8 using our custom function
gray_uint8 = im2uint8(gray)

# Show results
cv2.imshow("Original", gray)
cv2.imshow("After im2uint8", gray_uint8)
cv2.waitKey(0)
cv2.destroyAllWindows()
