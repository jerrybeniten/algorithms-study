import numpy as np

"""
1. What does im2uint8 do?
    If the image is already uint8 → it just returns the image as-is.
    If the image is floating-point (float32 or float64) → it assumes pixel values are in the range [0, 1] and scales them up to [0, 255].
    If the image is uint16 → it scales the range [0, 65535] down to [0, 255].
    This ensures that the output can be handled by most common image display functions, which expect uint8.

    When processing an image, the behavior 
    depends on its data type. If the image is 
    already in uint8 format, it’s returned 
    without changes. For floating-point images 
    (float32 or float64), it’s assumed that 
    pixel values are within the range [0, 1], 
    so they are scaled up to [0, 255]. 
    If the image is in uint16, the values 
    from [0, 65535] are scaled down to [0, 255]. 
    This normalization ensures that the 
    resulting image can be displayed correctly 
    by most common image viewing functions, 
    which typically expect uint8 data.

2. Effect on the appearance of the image
    If your image was already uint8 → no visible change.
    If your image was uint16 → you’ll see a similar image but with brightness correctly mapped to the smaller 0–255 range so that it displays properly. Without this scaling, a display function might show a very dark or completely black image.
    If your image was floating-point → values between 0 and 1 are mapped to 0–255, making them displayable.
    Basically, it makes the image look normal in an 8-bit viewer by adjusting intensity ranges.

    The impact on how an image appears depends 
    on its original format. If it's already in 
    uint8, there’s no noticeable difference. 
    For uint16 images, the brightness is adjusted 
    so that it fits within the 0–255 range, 
    ensuring it displays properly—without this 
    adjustment, the image might appear overly 
    dark or even entirely black. When working 
    with floating-point images, pixel values 
    between 0 and 1 are scaled to 0–255, 
    making them visible in standard image 
    viewers. In short, the process ensures 
    the image's brightness and contrast are 
    mapped correctly so it looks as intended 
    in an 8-bit display environment.

3. Effect on the elements of the image matrix
    Data type changes → from float or uint16 to uint8.
    Numeric range changes:
        float in [0, 1] → multiplied by 255, rounded down to integers.
        uint16 in [0, 65535] → divided by 257 to fit [0, 255].

    This process changes both the type of 
    data stored in the image and the 
    range of its values. If the image 
    starts as float or uint16, it’s converted 
    to uint8. For floating-point data in 
    the range 0 to 1, each value is multiplied 
    by 255 and then rounded down to the nearest 
    whole number. For uint16 data ranging from 
    0 to 65,535, the values are divided by 257 
    so they fit within 0 to 255. These 
    adjustments ensure the image data 
    matches the format expected by most 
    standard display and processing tools.

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