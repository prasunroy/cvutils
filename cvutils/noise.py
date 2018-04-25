# -*- coding: utf-8 -*-
"""
Noise models.
Created on Tue Apr 24 22:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
import cv2
import numpy
import random
from .validation import imvalidate


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
        density : Fraction of image pixels affected by noise. Only applicable
                  for Salt and Pepper noise model. Defaults to 0. Should be a
                  value between 0 and 1.
    
    Returns:
        A noisy image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    image = imvalidate(image)
    if not image is None:
        image = image.copy()
        
        if len(image.shape) == 2:
            image = numpy.expand_dims(image, 2)
        
        # get dimension of the image
        h, w = image.shape[:2]
        
        # apply a noise model
        model = model.upper()
        
        if model == 'GAUSSIAN':
            # Gaussian noise
            noise = numpy.random.normal(mu, sigma, (h, w))
            noise = numpy.dstack([noise]*image.shape[-1])
            image = image + noise
            image = cv2.normalize(image, None, 0, 255,
                                  cv2.NORM_MINMAX, cv2.CV_8UC1)
        
        elif model == 'SALT-AND-PEPPER':
            # Salt and Pepper noise
            if density < 0:
                density = 0
            elif density > 1:
                density = 1
            x = random.sample(range(w), w)
            y = random.sample(range(h), h)
            x, y = numpy.meshgrid(x, y)
            xy = numpy.c_[x.reshape(-1), y.reshape(-1)]
            n = int(w * h * density)
            n = random.sample(range(w*h), n)
            for i in n:
                if random.random() > 0.5:
                    image[xy[i][1], xy[i][0], :] = 255
                else:
                    image[xy[i][1], xy[i][0], :] = 0
            if image.shape[-1] == 1:
                image = numpy.squeeze(image, 2)
    
    return image
