import cv2
import numpy as np

# Step 1: Read the image
image = cv2.imread('input.jpeg')

# Step 2: Define sharpening kernel
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

# Step 3: Apply sharpening using filter2D
sharpened = cv2.filter2D(image, -1, kernel)

# Step 4: Show original and sharpened image
cv2.imshow('Original', image)
cv2.imshow('Sharpened', sharpened)
cv2.waitKey(0)
cv2.destroyAllWindows()
