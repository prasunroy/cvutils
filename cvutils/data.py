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
import requests

from scipy.io import savemat


# downloads images from ImageNet (http://www.image-net.org)
def fetch_imagenet(dst, wnids=[], limit=0, verbose=True):
    """Downloads images from ImageNet (http://www.image-net.org).
    
    Args:
        dst     : Destination directory for images.
        wnids   : A list of wnid strings of ImageNet synsets to download.
                  Defaults to an empty list.
        limit   : Maximum number of images to download from each specified
                  synset. Downloads all images if limit <= 0. Defaults to 0.
        verbose : Flag for verbose mode. Defaults to True.
    
    Returns:
        None.
    
    """
    api_url = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid='
    for wnid in wnids:
        # check directory
        path = os.path.join(dst, wnid)
        if not os.path.isdir(path):
            os.makedirs(path)
        
        # fetch image urls in synset
        if verbose:
            print('[INFO] Fetching image urls for synset {}... '.format(wnid), end='')
        urls = requests.get(api_url + wnid).content
        urls = urls.decode(encoding='utf-8').strip().split('\n')
        if verbose:
            print('got {} urls'.format(len(urls)))
        
        # download and save images
        count = 0
        if verbose:
            print('\r[INFO] Downloading images from synset {}... got {} images'.format(wnid, count), end='')
        for url in urls:
            try:
                image = bytearray(requests.get(url.strip()).content)
                image = numpy.asarray(image, dtype='uint8')
                image = cv2.imdecode(image, -1)
                if image is None:
                    raise Exception
                fname = str(count).zfill(len(str(len(urls)))) + '.jpg'
                cv2.imwrite(os.path.join(path, fname), image)
            except:
                continue
            count += 1
            if verbose:
                print('\r[INFO] Downloading images from synset {}... got {} images'.format(wnid, count), end='')
            if limit > 0 and count >= limit:
                break
        if verbose:
            print('')
    if verbose:
        print('[INFO] Download complete')
    
    return


# builds labeled dataset from structurally organized images
def build_data(src, dst, flag=1, size=(128, 128), length=10000, verbose=True):
    """Builds labeled dataset from structurally organized images.
    
    Args:
        src     : Source directory of labeled images. It should contain all the
                  labels as sub-directories where name of each sub-directory is
                  one class label and all images inside that sub-directory are
                  instances of that class.
        dst     : Destination directory for labelmap and data files.
        flag    : Read flag. Defaults to 1.
                  >0 -- read as color image (ignores alpha channel)
                  =0 -- read as grayscale image
                  <0 -- read as original image (keeps alpha channel)
        size    : Target size of images. Defaults to (128, 128).
        length  : Maximum number of images to be written in one data file.
                  Defaults to 10000.
        verbose : Flag for verbose mode. Defaults to True.
    
    Returns:
        None.
    
    Yields:
        A labelmap.json file containing mapping of labels into numeric class
        ids and one or more .mat files containing labeled data. Each row of the
        data is one labeled sample where the first column is a numeric class id
        and the remaining columns are one dimensional representation of the
        image pixels.
    
    """
    # validate arguments
    if not _validate_args(src, dst, flag, size, length, verbose):
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
    part = 0
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
            if len(data) >= length:
                _save(dst, data, part)
                data = []
                part += 1
    if len(data) > 0:
        if part > 0:
            _save(dst, data, part)
        else:
            _save(dst, data)
    if verbose:
        print('[INFO] Build complete')
    
    return


# validates arguments
def _validate_args(src, dst, flag, size, length, verbose):
    if type(verbose) is not bool and type(verbose) is not int:
        print('[INFO] Verbose flag must be either a boolean or an integer')
        return False
    if not os.path.isdir(src):
        if verbose:
            print('[INFO] Image source directory not found')
        return False
    if not os.path.isdir(dst):
        os.makedirs(dst)
    elif len(os.listdir(dst)) > 0:
        if verbose:
            print('[INFO] Data destination must be an empty directory')
        return False
    if type(flag) is not int:
        if verbose:
            print('[INFO] Read flag must be an integer')
        return False
    if len(size) != 2 or type(size[0]) is not int or type(size[1]) is not int \
    or size[0] <= 0 or size[1] <= 0:
        if verbose:
            print('[INFO] Target size must be a positive integer 2-tuple')
        return False
    if type(length) is not int or length <= 0:
        if verbose:
            print('[INFO] Length of each partition must be a positive integer')
        return False
    
    return True


# saves data
def _save(dst, data, part=-1):
    if part < 0:
        file = os.path.join(dst, 'data.mat')
    else:
        file = os.path.join(dst, 'data_{}.mat'.format(str(part).zfill(4)))
    data = numpy.asarray(data, dtype='uint8')
    
    savemat(file, {'data': data})
    
    return
