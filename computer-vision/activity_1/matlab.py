import numpy as np

"""
1. What does im2uint8 do?
    If the image is already uint8 → it just returns the image as-is.
    If the image is floating-point (float32 or float64) → it assumes pixel values are in the range [0, 1] and scales them up to [0, 255].
    If the image is uint16 → it scales the range [0, 65535] down to [0, 255].
    This ensures that the output can be handled by most common image display functions, which expect uint8.

2. Effect on the appearance of the image
    If your image was already uint8 → no visible change.
    If your image was uint16 → you’ll see a similar image but with brightness correctly mapped to the smaller 0–255 range so that it displays properly. Without this scaling, a display function might show a very dark or completely black image.
    If your image was floating-point → values between 0 and 1 are mapped to 0–255, making them displayable.
    Basically, it makes the image look normal in an 8-bit viewer by adjusting intensity ranges.

3. Effect on the elements of the image matrix
    Data type changes → from float or uint16 to uint8.
    Numeric range changes:
        float in [0, 1] → multiplied by 255, rounded down to integers.
        uint16 in [0, 65535] → divided by 257 to fit [0, 255].

Precision loss:
    16-bit and floating-point images store more intensity levels than uint8.
    Converting to uint8 means fewer shades (only 256 levels), so subtle gradients might get slightly banded.
"""
def im2uint8(image):
    """
    Replicates MATLAB's im2uint8() behavior in Python using NumPy.
    Parameters: image (np.ndarray): Input image (float [0,1], uint16 [0,65535], or uint8)
    Returns:np.ndarray: Image converted to uint8 [0,255]
    """

    if image.dtype == np.uint8:
        # Already uint8, return as-is
        return image

    elif np.issubdtype(image.dtype, np.floating):
        # Floating-point image: expected range [0, 1]
        image = np.clip(image, 0, 1)  # Ensure within [0,1]
        return (image * 255).astype(np.uint8)

    elif image.dtype == np.uint16:
        # 16-bit image: scale from [0,65535] to [0,255]
        return (image / 257).astype(np.uint8)  # 65535 / 255 ≈ 257

    else:
        raise TypeError(f"Unsupported image dtype: {image.dtype}")