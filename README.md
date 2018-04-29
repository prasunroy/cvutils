# cvutils
**A collection of commonly used computer vision functions based on OpenCV and Python.**
<img align='right' height='100' src='https://github.com/prasunroy/cvutils/blob/master/assets/logo.png' />

![badge](https://github.com/prasunroy/cvutils/blob/master/assets/badge_1.svg)
![badge](https://github.com/prasunroy/cvutils/blob/master/assets/badge_2.svg)

## Installation
#### Method 1: Install using native pip
```
pip install git+https://github.com/prasunroy/cvutils.git
```
#### Method 2: Install manually
```
git clone https://github.com/prasunroy/cvutils.git
cd cvutils
python setup.py install
```

## Image Input-Output Functions
### Read image
#### Description
```
imread(path, flag=-1)
    Reads an image file.

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
```
#### Example
```python
from cvutils.io import imread
from cvutils.io import imshow

# read an image file
image = imread('ArcticFox.jpg')
imshow(image, title='Read from image file')

# read an image url
image = imread('https://github.com/prasunroy/cvutils/raw/master/assets/Kingfisher.jpg')
imshow(image, title='Read from image url')
```

<img src='https://github.com/prasunroy/cvutils/raw/master/assets/image_1.png' />

### Write image
#### Description
```
imwrite(path, image)
    Writes an image file.

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
```
#### Example
```python
from cvutils.io import imread
from cvutils.io import imwrite

# read a JPEG image file as grayscale and write to a PNG image file
image = imread('Kingfisher.jpg', flag=0)
imwrite('Kingfisher.png', image)
```

### Show image
#### Description
```
imshow(image, title='')
    Shows an image in a window.

    Args:
        image : Image source. This can be either a numpy array, a path to an
                image file or an image url.
        title : Window title. Defaults to an empty string.

    Returns:
        None
```
#### Example
```python
from cvutils.io import imread
from cvutils.io import imshow

# show an image file
imshow('ArcticFox.jpg', title='Color image')

# show an image url
imshow('https://github.com/prasunroy/cvutils/raw/master/assets/Kingfisher.jpg', title='Color image')

# read an image file as grayscale and show
image = imread('ArcticFox.jpg', flag=0)
imshow(image, title='Grayscale image')

# read an image url as grayscale and show
image = imread('https://github.com/prasunroy/cvutils/raw/master/assets/Kingfisher.jpg', flag=0)
imshow(image, title='Grayscale image')
```

<img src='https://github.com/prasunroy/cvutils/raw/master/assets/image_2.png' />

## Noise Models
### Apply a noise model to an image
#### Description
```
imnoise(image, model, mu=0, sigma=0, density=0)
    Applies a noise model to an image.

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
```
#### Example
```python
from cvutils.io import imread
from cvutils.io import imshow
from cvutils.noise import imnoise

# read images
image1 = imread('ArcticFox.jpg')
image2 = imread('Kingfisher.jpg')

# apply addtive white Gaussian noise
noisy1_awgn = imnoise(image1, model='Gaussian', mu=0, sigma=25)
noisy2_awgn = imnoise(image2, model='Gaussian', mu=0, sigma=50)

# apply salt and pepper noise
noisy1_snpn = imnoise(image1, model='Salt-and-Pepper', density=0.05)
noisy2_snpn = imnoise(image2, model='Salt-and-Pepper', density=0.10)

# show results
imshow(image1, title='Original image')
imshow(noisy1_awgn, title='Gaussian noise')
imshow(noisy1_snpn, title='Salt and Pepper noise')

imshow(image2, title='Original image')
imshow(noisy2_awgn, title='Gaussian noise')
imshow(noisy2_snpn, title='Salt and Pepper noise')
```

<img src='https://github.com/prasunroy/cvutils/raw/master/assets/image_3.png' />

## References
>[ArcticFox.jpg](https://github.com/prasunroy/cvutils/raw/master/assets/ArcticFox.jpg) and [Kingfisher.jpg](https://github.com/prasunroy/cvutils/raw/master/assets/Kingfisher.jpg) are obtained from [Pixabay](https://pixabay.com) made available under [Creative Commons CC0 License](https://creativecommons.org/publicdomain/zero/1.0/deed.en).

>This work is inspired by [Adrian Rosebrock](https://github.com/jrosebr1)'s work on [imutils](https://github.com/jrosebr1/imutils) package.

## License
MIT License

Copyright (c) 2018 Prasun Roy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<br />
<br />

**Made with** :heart: **and GitHub**
