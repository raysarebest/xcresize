# Xcode Asset Resizer

Specify a 3x scale image you want to use in an app you're making with Xcode, and this will output a valid `.iconset` bundle to drop into your filesystem

## Setup

This project requires [Pillow](https://python-pillow.org), an updated fork of the [Python Imaging Library](https://en.wikipedia.org/wiki/Python_Imaging_Library). You can learn how to install it in [their documentation](http://pillow.readthedocs.io/en/3.0.x/installation.html), but the TL;DR is that you can probably just run `pip install Pillow`. This project also requires Python 3.6 or newer.