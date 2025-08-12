import numpy as np

def hsi_to_rgb(H, S, I):
    H = np.deg2rad(H)  # Convert degrees to radians

    # Prepare output
    R = np.zeros_like(H)
    G = np.zeros_like(H)
    B = np.zeros_like(H)

    # RG Sector (0°–120°)
    mask1 = (H >= 0) & (H < 2*np.pi/3)
    B[mask1] = I[mask1] * (1 - S[mask1])
    R[mask1] = I[mask1] * (1 + (S[mask1] * np.cos(H[mask1]) / np.cos(np.pi/3 - H[mask1])))
    G[mask1] = 3 * I[mask1] - (R[mask1] + B[mask1])

    # GB Sector (120°–240°)
    mask2 = (H >= 2*np.pi/3) & (H < 4*np.pi/3)
    H2 = H[mask2] - 2*np.pi/3
    R[mask2] = I[mask2] * (1 - S[mask2])
    G[mask2] = I[mask2] * (1 + (S[mask2] * np.cos(H2) / np.cos(np.pi/3 - H2)))
    B[mask2] = 3 * I[mask2] - (R[mask2] + G[mask2])

    # BR Sector (240°–360°)
    mask3 = (H >= 4*np.pi/3) & (H < 2*np.pi)
    H3 = H[mask3] - 4*np.pi/3
    G[mask3] = I[mask3] * (1 - S[mask3])
    B[mask3] = I[mask3] * (1 + (S[mask3] * np.cos(H3) / np.cos(np.pi/3 - H3)))
    R[mask3] = 3 * I[mask3] - (G[mask3] + B[mask3])

    # Scale to 0–255 and clip
    R = np.clip(R * 255, 0, 255).astype(np.uint8)
    G = np.clip(G * 255, 0, 255).astype(np.uint8)
    B = np.clip(B * 255, 0, 255).astype(np.uint8)

    return R, G, B

# Example
H = np.array([210.0])
S = np.array([0.333])
I = np.array([0.588])

R, G, B = hsi_to_rgb(H, S, I)
print(f"RGB: ({R[0]}, {G[0]}, {B[0]})")
