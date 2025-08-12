import cv2
import numpy as np

def rgb_to_hsi(image):
    # Convert to float and normalize to [0,1]
    img = image.astype(np.float32) / 255.0
    R, G, B = img[:,:,2], img[:,:,1], img[:,:,0]  # OpenCV loads in BGR order
    
    # Intensity
    I = (R + G + B) / 3.0
    
    # Saturation
    min_rgb = np.minimum(np.minimum(R, G), B)
    S = 1 - (3 / (R + G + B + 1e-6)) * min_rgb  # +1e-6 to avoid division by zero
    
    # Hue calculation
    num = 0.5 * ((R - G) + (R - B))
    den = np.sqrt((R - G)**2 + (R - B)*(G - B)) + 1e-6
    theta = np.arccos(np.clip(num / den, -1, 1))  # Clip for numerical stability
    
    H = np.where(B <= G, theta, 2*np.pi - theta)
    H = np.degrees(H)  # Convert to degrees
    
    # Stack into HSI image
    HSI = cv2.merge((H, S, I))
    return HSI

if __name__ == "__main__":
    # Create an image with RGB(100, 150, 200)
    rgb_color = (100, 150, 200)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[:] = (rgb_color[2], rgb_color[1], rgb_color[0])  # BGR for OpenCV
    
    hsi_img = rgb_to_hsi(img)
    
    # Print the HSI values for the first pixel
    H_val, S_val, I_val = hsi_img[0,0]
    print(f"HSI Values for RGB{rgb_color}:")
    print(f"Hue: {H_val:.2f}°")
    print(f"Saturation: {S_val:.3f}")
    print(f"Intensity: {I_val:.3f}")
    
    # Display images
    cv2.imshow("Original RGB", img)
    cv2.imshow("Hue", hsi_img[:,:,0] / 360)  # Normalize hue for display
    cv2.imshow("Saturation", hsi_img[:,:,1])
    cv2.imshow("Intensity", hsi_img[:,:,2])
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
