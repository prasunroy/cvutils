# -*- coding: utf-8 -*-
"""
Image input-output functions.
Created on Thu Apr 19 22:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
import cv2
import numpy
import os
import requests
from .validation import imvalidate


# reads an image file
def imread(path, flag=-1):
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
        path : Path to an image file or an image url.
        flag : Read flag. Defaults to -1.
               >0 -- read as color image (ignores alpha channel)
               =0 -- read as grayscale image
               <0 -- read as original image (keeps alpha channel)
    
    Returns:
        An image as a numpy array if read is successful None otherwise.
        The order of channels is BGR(A) for color image.
    
    """
    image = None
    try:
        if os.path.exists(path):
            image = cv2.imread(path, flag)
        else:
            image = bytearray(requests.get(path).content)
            image = numpy.asarray(image, dtype='uint8')
            image = cv2.imdecode(image, flag)
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
        image = imvalidate(image)
        if not image is None:
            cv2.imwrite(path, image)
            flag = True
    except:
        pass
    
    return flag


# shows an image in a window
def imshow(image, title=''):
    """Shows an image in a window.
    
    Args:
        image : Image source. This can be either a numpy array, a path to an
                image file or an image url.
        title : Window title. Defaults to an empty string.
    
    Returns:
        None
    
    """
    try:
        array = imvalidate(image)
        if array is None:
            array = imread(image, -1)
            array = imvalidate(array)
        if not array is None:
            cv2.imshow(str(title), array)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    except:
        pass
    
    return
