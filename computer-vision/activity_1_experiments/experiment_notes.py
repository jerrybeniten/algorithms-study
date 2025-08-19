"""
C000_one_pixel_gray_opencv.png = 536 bits
C128_one_pixel_gray_opencv.png = 536 bits

Gray Scale
C255_one_pixel_gray_opencv.webp =  304 bits |   38 bytes | lossy predictive data. developed by google, also good for web.
C255_one_pixel_gray_opencv.png  =  536 bits |   67 bytes | lossless - compression is efficient good for web.
C255_one_pixel_gray_opencv.jpeg = 2664 bits |  333 bytes | lossy    - lots of metadata stored good for print.
C255_one_pixel_gray_opencv.bmp  = 8656 bits | 1082 bytes | uncompressed - stores raw pixel value.

Using Binary Image
CTRUE_one_pixel_binary_opencv.png  =  536 bits |   67 bytes
CTRUE_one_pixel_binary_opencv.jpeg = 2664 bits |  333 bytes
CTRUE_one_pixel_binary_opencv.bmp  = 8656 bits | 1082 bytes

Indexed Image
C255_one_pixel_indexed_opencv.bmp  =  464 bits |  58 bytes
C255_one_pixel_indexed_opencv.png  =  552 bits |  69 bytes
C255_one_pixel_indexed_opencv.jpeg = 5048 bits | 631 bytes

True Color Image
C255_one_pixel_truecolor_opencv.bmp  =  464 bits |  58 bytes
C255_one_pixel_truecolor_opencv.png  =  552 bits |  69 bytes
C255_one_pixel_truecolor_opencv.jpeg = 5048 bits | 631 bytes

EXPLAINATION TO INDEXED IMAGE
1. BMP – 464 bits (58 bytes)

BMP is uncompressed (except RLE modes, which you’re not using here).

Even for 1 pixel, BMP has a fixed header (14 bytes) + DIB header (40 bytes) + palette + pixel data.

In your case:

14 bytes  (BMP file header)
40 bytes  (DIB header)
 4 bytes  (palette entry for white — each color is 4 bytes)
 ...


That overhead explains why even a single pixel ends up 58 bytes.

2. PNG – 552 bits (69 bytes)

PNG uses lossless compression (DEFLATE), so repeated patterns are compressed very well.
For a 1-pixel indexed PNG, the actual pixel data is tiny, but PNG also stores:
PNG header (89 50 4E 47 magic number)
IHDR chunk (width, height, bit depth, etc.)
PLTE chunk (the palette)
IDAT chunk (compressed pixel data)
IEND chunk

Since compression doesn’t help much with 1 pixel, the file is mostly metadata overhead.

3. JPEG – 5048 bits (631 bytes)
JPEG is a lossy compression format meant for continuous-tone images, not indexed colors.
It cannot store a palette, so OpenCV first converts your indexed image to RGB before saving.
Then, the RGB image is processed through JPEG’s block-based compression (8×8 minimum block size).
Even though the image is only 1×1, JPEG internally pads it to 8×8 pixels in the DCT stage — meaning it stores an entire 64-pixel block.
This block + JPEG’s Huffman tables, quantization tables, and metadata = huge overhead for such a tiny image.


Reason why it is called uint8 is because 255 = total of 8 bits

128 64  32  16  8   4   2   1
1   1   1   1   1   1   1   1 = 255 (WHITE)

128 64  32  16  8   4   2   1
0   0   0   0   0   0   0   0 =   0 (BLACK)


"""