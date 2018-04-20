"""
Image input-output functions.
Created on Thu Apr 19 22:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
import cv2


# reads an image file
def imread(path, flag=1):
    """Reads an image file.
    
    Supported image file formats:
        Bitmap    : *.bmp, *.dib
        JPEG      : *.jpe, *.jpeg, *.jpg
        JPEG 2000 : *.jp2
        PNG       : *.png
        Portable  : *.pbm, *.pgm, *.ppm
        Raster    : *.ras, *.sr
        TIFF      : *.tif, *.tiff
        WebP      : *.webp
    
    Args:
        path (str) : Path to the image file.
        flag (int) : Read flag. Defaults to 1.
                     >0 -- read as color image (ignores alpha channel)
                     =0 -- read as grayscale image
                     <0 -- read as color image (keeps alpha channel)
    
    Returns:
        A numpy array if read is successful None otherwise. The order of
        channels is BGR(A) when reading as color image.
    
    """
    image = None
    try:
        image = cv2.imread(path, flag)
    except:
        pass
    
    return image


# writes an image file
def imwrite(path, image):
    """Writes an image file.
    
    Supported image file formats:
        Bitmap    : *.bmp, *.dib
        JPEG      : *.jpe, *.jpeg, *.jpg
        JPEG 2000 : *.jp2
        PNG       : *.png
        Portable  : *.pbm, *.pgm, *.ppm
        Raster    : *.ras, *.sr
        TIFF      : *.tif, *.tiff
        WebP      : *.webp
    
    Args:
        path  : Path to the image file to be written. If the file already
                exists it will be overwritten.
        image : A numpy array. The order of channels is BGR(A) for color image.
    
    Returns:
        True if write is successful False otherwise.
    
    """
    flag = False
    try:
        cv2.imwrite(path, image)
        flag = True
    except:
        pass
    
    return flag
