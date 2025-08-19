import cv2
import matplotlib.pyplot as plt

# Load the cameraman image in grayscale
y = cv2.imread("cameraman.tif", cv2.IMREAD_GRAYSCALE)

# Add 128 to the image using OpenCV (handles clipping at 255)
y_added = cv2.subtract(y, 128)

# Show original and new image side by side
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.title("Original Image")
plt.imshow(y, cmap="gray")
plt.axis("off")

plt.subplot(1,2,2)
plt.title("After imadd(y, 128)")
plt.imshow(y_added, cmap="gray")
plt.axis("off")
plt.show()
