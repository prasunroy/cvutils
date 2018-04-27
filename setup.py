# -*- coding: utf-8 -*-
"""
Setup script.
Created on Fri Apr 27 00:00:00 2018
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/cvutils

"""


# imports
from setuptools import setup, find_packages


# setup
setup(name='cvutils',
      version='0.1.0',
      description='A collection of commonly used computer vision functions based on OpenCV and Python',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Prasun Roy',
      author_email='prasunroy.pr@gmail.com',
      url='https://github.com/prasunroy/cvutils',
      download_url='github.com/prasunroy/cvutils/tarball/0.1.0',
      license='MIT',
      install_requires=[
              'numpy',
              'opencv-python>=3.4.0',
              'requests'
      ],
      classifiers=[
              'Development Status :: 4 - Beta',
              'Intended Audience :: Education',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: MIT License',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.6',
              'Topic :: Scientific/Engineering',
              'Topic :: Software Development :: Libraries',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Utilities'
      ],
      keywords=[
              'computer-vision',
              'image-processing'
      ],
      packages=find_packages())
