import os

file_path = "C255_one_pixel_gray_opencv.webp"  # change if needed
file_size_bits = os.path.getsize(file_path) * 8
print(f"File size: {file_size_bits} bits")
