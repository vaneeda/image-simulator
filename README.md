# Simulated images

Randomly select a background image and object images, and paste them
around to create new images.  Useful (one would hope) for generating
training data for neural networks/deep learning.

## Usage

    python3 imagesim.py -n N [-e E] [-s] -b <bgs> -c <cs> -o <out>

Where

- N is number of images to generate
- E is the max number of objects per image (default 6)
- s is whether to use only a single class of objects per image, or allow
  a mixture
- bgs is a directory of background images
- cs is a directory containing directories of classes
- out is the output directory
