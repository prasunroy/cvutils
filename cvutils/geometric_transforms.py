# -*- coding: utf-8 -*-
"""
Geometric image transformation functions.
Created on Sat Apr 21 21:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
import cv2
import numpy


# translation
def translate(image, tx=0, ty=0):
    """Translates an image by a specified shift.
    
    Args:
        image : An image as a numpy array.
        tx    : Translation along x-axis in pixels. Defaults to 0.
        ty    : Translation along y-axis in pixels. Defaults to 0.
    
    Returns:
        The translated image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    T = None
    image = validate(image)
    if not image is None:
        # get dimension of the image
        h, w = image.shape[:2]
        
        # construct transformation matrix and translate the image
        M = numpy.float32([[1, 0, tx], [0, 1, ty]])
        T = cv2.warpAffine(image, M, (w, h))
    
    return T


# rotation
def rotate(image, angle=0):
    """Rotates an image by a specified angle.
    
    Args:
        image : An image as a numpy array.
        angle : Angle of rotation around center of the image in degree.
                Defaults to 0.
    
    Returns:
        The rotated image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    R = None
    image = validate(image)
    if not image is None:
        # get dimension of the image
        h, w = image.shape[:2]
        
        # calculate center of the image
        center = (w/2, h/2)
        
        # construct transformation matrix and rotate the image
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        R = cv2.warpAffine(image, M, (w, h))
    
    return R


# scaling
def scale(image, size=(-1, -1)):
    """Scales an image into a specified dimension.
    
    Args:
        image : An image as a numpy array.
        size  : Size of the scaled image as integer tuple (width, height).
                Preserves aspect ratio after scaling if either width or height
                is <= 0. Does not perform scaling if both width and height
                are <= 0. Defaults to (-1, -1).
    
    Returns:
        The scaled image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    S = None
    image = validate(image)
    if not image is None:
        S = image
        
        # get dimension of the image
        h, w = image.shape[:2]
        
        # calculate aspect ratio of the image as width:height
        r = w / h
        
        # get dimension of the scaled image
        sw, sh = size
        
        # calculate dimension of the scaled image
        if sw > 0 and sh <= 0:
            sh = int(sw / r)
        elif sw <= 0 and sh > 0:
            sw = int(sh * r)
        
        # scale image
        if sw > 0 and sh > 0:
            S = cv2.resize(image, (sw, sh))
    
    return S


# validates an input as image
def validate(src):
    """Validates an input as image.
    
    Args:
        src : Input to be validated.
    
    Returns:
        A numpy array if the input is a valid image None otherwise.
    
    """
    image = None
    if type(src) is numpy.ndarray and src.size > 0:
        dims = len(src.shape)
        if dims == 1:
            image = numpy.expand_dims(src, 1)
        elif dims == 2 or (dims == 3 and src.shape[-1] in [1, 3, 4]):
            image = src
    
    return image
