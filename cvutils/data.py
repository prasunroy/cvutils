# -*- coding: utf-8 -*-
"""
Image data building functions.
Created on Thu May 17 22:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
from __future__ import print_function

import cv2
import glob
import json
import numpy
import os

from scipy.io import savemat


# builds labeled dataset from structurally organized images
def build_data(src, dst, flag=1, size=(128, 128), verbose=True):
    """Builds labeled dataset from structurally organized images.
    
    """
    # verify paths
    if not os.path.isdir(src):
        if verbose:
            print('[INFO] Image source directory not found')
        return
    if not os.path.isdir(dst):
        os.makedirs(dst)
    elif len(os.listdir(dst)) > 0:
        if verbose:
            print('[INFO] Data destination must be an empty directory')
        return
    
    # class labels
    labels = [os.path.split(d[0])[-1] for d in os.walk(src)][1:]
    
    # map labels into numeric class ids
    labelmap = {key:value for key, value in zip(labels, range(len(labels)))}
    
    # save labelmap
    if len(labelmap.keys()) > 0:
        with open(os.path.join(dst, 'labelmap.json'), 'w') as file:
            json.dump(labelmap, file)
        if verbose:
            print('[INFO] Created labelmap')
    
    # build data
    data = []
    for label in labels:
        files = glob.glob(os.path.join(src, label, '*.*'))
        for file in files:
            image = cv2.imread(file, flag)
            if image is None:
                continue
            if verbose:
                print('[INFO] Processing {}'.format(file))
            x = cv2.resize(image, size).reshape(-1)
            y = labelmap[label]
            data.append(numpy.r_[y, x])
    data = numpy.asarray(data, dtype='uint8')
    savemat(os.path.join(dst, 'data.mat'), {'data': data})
    if verbose:
        print('[INFO] Build complete')
    
    return
