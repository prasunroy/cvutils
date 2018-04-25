# -*- coding: utf-8 -*-
"""
Validation functions.
Created on Wed Apr 25 21:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
import numpy


# validates a numpy array as an image
def imvalidate(array):
    """Validates a numpy array as an image.
    
    Args:
        array : A numpy array to be validated.
    
    Returns:
        An image as a numpy array if validation is successful None otherwise.
    
    """
    image = None
    if type(array) is numpy.ndarray and array.size > 0:
        dims = len(array.shape)
        if dims == 1:
            image = numpy.expand_dims(array, 1)
        elif dims == 2 or (dims == 3 and array.shape[-1] in [1, 3, 4]):
            image = array
    
    return image
