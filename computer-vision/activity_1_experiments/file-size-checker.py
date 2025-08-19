import os

file_path = "one_pixel_red_grayscale_uint8.tiff"  # change if needed
file_size_bits = os.path.getsize(file_path) * 8
print(f"File size: {file_size_bits} bits")
