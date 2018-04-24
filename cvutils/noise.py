# -*- coding: utf-8 -*-
"""
Noise models.
Created on Tue Apr 24 22:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
import numpy


# applies a noise model to an image
def imnoise(image, model, mu=0, sigma=0, density=0):
    """Applies a noise model to an image.
    
    Args:
        image   : An image as a numpy array.
        model   : A noise model as a string.
                  ='Gaussian'        -- applies Gaussian noise model
                  ='Salt-and-Pepper' -- applies Salt and Pepper noise model
        mu      : Mean of Gaussian distribution. Only applicable for Gaussian
                  noise model. Defaults to 0.
        sigma   : Standard deviation of Gaussian distribution. Only applicable
                  for Gaussian noise model. Defaults to 0.
        density : Approximate fraction of image pixels affected by noise. Only
                  applicable for Salt and Pepper noise model.
    
    Returns:
        A noisy image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    image = None
    image = validate(image)
    if not image is None:
        model = model.upper()
        if model == 'GAUSSIAN':
            pass
        elif model == 'SALT-AND-PEPPER':
            pass
    
    return image


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
