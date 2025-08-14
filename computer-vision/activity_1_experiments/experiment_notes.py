"""
C000_one_pixel_gray_opencv.png = 536 bits
C128_one_pixel_gray_opencv.png = 536 bits

C255_one_pixel_gray_opencv.webp =  304 bits |   38 bytes | lossy predictive data. developed by google, also good for web.
C255_one_pixel_gray_opencv.png  =  536 bits |   67 bytes | lossless - compression is efficient good for web.
C255_one_pixel_gray_opencv.jpeg = 2664 bits |  333 bytes | lossy    - lots of metadata stored good for print.
C255_one_pixel_gray_opencv.bmp  = 8656 bits | 1082 bytes | uncompressed - stores raw pixel value.

Reason why it is called uint8 is because 255 = total of 8 bits

128 64  32  16  8   4   2   1
1   1   1   1   1   1   1   1 = 255 (WHITE)

128 64  32  16  8   4   2   1
0   0   0   0   0   0   0   0 =   0 (BLACK)


"""