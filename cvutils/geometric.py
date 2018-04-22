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
        size  : Size of the scaled image as an integer tuple (width, height).
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


# affine transform
def affine(image, src, dst):
    """Performs affine transformation on an image.
    
    Args:
        image : An image as a numpy array.
        src   : Three points on the image either as a list of three tuples
                [(x0, y0), (x1, y1), (x2, y2)] or as a 3x2 numpy array
                [[x0, y0], [x1, y1], [x2, y2]].
        dst   : Three points on the image either as a list of three tuples
                [(x0, y0), (x1, y1), (x2, y2)] or as a 3x2 numpy array
                [[x0, y0], [x1, y1], [x2, y2]].
                The Points on the transformed image (dst) exactly correspond to
                the points on the input image (src).
    
    Returns:
        The transformed image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    A = None
    image = validate(image)
    if not image is None:
        # get dimension of the image
        h, w = image.shape[:2]
        
        # convert src and dst into numpy arrays
        src = numpy.float32(src)
        dst = numpy.float32(dst)
        
        # construct transformation matrix and perform affine transformation
        M = cv2.getAffineTransform(src, dst)
        A = cv2.warpAffine(image, M, (w, h))
    
    return A


# perspective transform
def perspective(image, src, dst):
    """Performs perspective transformation on an image.
    
    Args:
        image : An image as a numpy array.
        src   : Four points on the image either as a list of four tuples
                [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] or as a 4x2 numpy
                array [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]. At least three
                of these four points should be non-collinear.
        dst   : Four points on the image either as a list of four tuples
                [(x0, y0), (x1, y1), (x2, y2), (x3, y3)] or as a 4x2 numpy
                array [[x0, y0], [x1, y1], [x2, y2], [x3, y3]].
                The Points on the transformed image (dst) exactly correspond to
                the points on the input image (src).
    
    Returns:
        The transformed image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    P = None
    image = validate(image)
    if not image is None:
        # get dimension of the image
        h, w = image.shape[:2]
        
        # convert src and dst into numpy arrays
        src = numpy.float32(src)
        dst = numpy.float32(dst)
        
        # construct transformation matrix and perform perspective
        # transformation
        M = cv2.getPerspectiveTransform(src, dst)
        P = cv2.warpPerspective(image, M, (w, h))
    
    return P


# four point perspective transform
def perspective4P(image, points):
    """Performs perspective transformation on an image
       using four corner points.
    
    Args:
        image  : An image as a numpy array.
        points : Four corner points of the image either as a list of four
                 tuples (x, y) or as a 4x2 numpy array.
    
    Returns:
        The transformed image as a numpy array if the input is a valid image
        None otherwise.
    
    """
    P = None
    image = validate(image)
    if not image is None:
        # order four corner points
        src = numpy.float32(points)
        src = sort4P(src)
        
        # calculate maximum width and height of the bounding rectangle
        # formed by the four corner points
        w = int(max(distance(src[0], src[1])[0], distance(src[2], src[3])[0]))
        h = int(max(distance(src[0], src[3])[0], distance(src[1], src[2])[0]))
        
        # construct four corner points which will be the new corner points
        # after the perspective transformation
        dst = numpy.float32([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]])
        
        # calculate transformation matrix and perform perspective
        # transformation
        M = cv2.getPerspectiveTransform(src, dst)
        P = cv2.warpPerspective(image, M, (w, h))
    
    return P


# sort four corner points of a quadrilateral
def sort4P(points):
    """Sorts four corner points of a quadrilateral in clockwise order of
       top-left, top-right, bottom-right, bottom-left.
    
    Args:
        points : Four corner points of a quadrilateral either as a list of four
                 tuples (x, y) or as a 4x2 numpy array.
    
    Returns:
        Four sorted corner points either as a list or as a numpy array
        depending upon the input format.
    
    """
    P = numpy.float32(points)
    assert P.shape == (4, 2)
    
    # sort points based on x coordinate
    S = P[P[:, 0].argsort()]
    
    # left and right corners
    L = S[:2]
    R = S[2:]
    
    # sort left and right corners based on y coordinate
    L = L[L[:, 1].argsort()]
    R = R[R[:, 1].argsort()]
    
    # order corners in top-left, top-right, bottom-right, bottom-left
    if type(points) is list:
        P = [tuple(L[0]), tuple(R[0]), tuple(R[1]), tuple(L[1])]
    elif type(points) is numpy.ndarray:
        P[0] = L[0]
        P[1] = R[0]
        P[2] = R[1]
        P[3] = L[1]
    
    return P


# distance metrics
def distance(p, q):
    """Calculates Euclidean, D4 and D8 distances between two points.
    
    Args:
        p : The first point. Either a tuple, a list or an array.
        q : The second point. Either a tuple, a list or an array.
    
    Returns:
        A list containing Euclidean, D4 and D8 distances between p and q.
    
    """
    p = numpy.asarray(p).reshape(-1)
    q = numpy.asarray(q).reshape(-1)
    assert p.size == q.size
    
    # calculate absolute difference
    d = numpy.abs(p-q)
    
    # calculate Euclidean distance
    dE = numpy.sqrt(numpy.sum(d**2))
    
    # calculate D4 distance
    d4 = numpy.sum(d)
    
    # calculate D8 distance
    d8 = numpy.max(d)
    
    return [dE, d4, d8]


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
