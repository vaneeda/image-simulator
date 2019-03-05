import sys
# check if python3 is used
if sys.version_info < (3, 0):
    print("This programs need python3x to run. Aborting.")
    sys.exit(1)

import os
import random
from PIL import Image
from math import floor

def initialize(backgrounds_dir, classes_dir):
    # Loading data
    backgrounds = os.listdir(backgrounds_dir)
    class_names = os.listdir(classes_dir)
    class_objects = [os.listdir(os.path.join(classes_dir,c)) for c in class_names]

    # ignore scaling for now: .resize(resolution, Image.BICUBIC)
    bgs = [Image.open(os.path.join(backgrounds_dir,b)) for b in backgrounds]

    objs = []
    for i,c in enumerate(class_objects):
        print('loading '+class_names[i]+' as '+str(i))
        objs = objs + [[Image.open(os.path.join(classes_dir,class_names[i],o)) for o in c]]

    return objs, class_names, bgs

# Simulate an image
def mkimage(filename, objs, names, bgs, maxobjs, output_dir="images_out",single=False):
    """
    Generates a synthetic image consisting of a random number of objects pasted on a random background
    and a text file with coordinates of each object, along with class name.

    Parameters:
    :param filename: Prefix of image and text file generated
    :param objs: List of lists of image crops
    :param names: Class names
    :param bgs: Directory of background images
    :param maxobjs: Maximum number of objects generated in a given image
    :param output_dir: Output directory, default="images_out"
    :param single: Boolean indicating whether image contains a single species (True) or not

    :Returns: png image and txt file
    """

    log = []
    im = bgs[random.randint(0,len(bgs)-1)].copy()
    # print('bg size='+str(im.size))
    cls0 = random.randint(0,len(objs)-1)
    for c in range(0, random.randint(1, maxobjs)):

        if single: cls=cls0
        else: cls = random.randint(0,len(objs)-1)
        obj = random.choice(objs[cls])
        sizex,sizey = obj.size
        imx,imy = im.size
        posx = random.randint(-floor(sizex/2),imx-floor(sizex/2))
        posy = random.randint(-floor(sizey/2),imy-floor(sizey/2))
        im.paste(obj,(posx,posy),obj)
        log = log + ['{}\t{}\t{}\t{}\t{}\t{}\n'.format(names[cls],cls,posy,posx,posy+sizey,posx+sizex)]
    im.save(os.path.join(output_dir,filename+'.png'))
    with open(os.path.join(output_dir,filename+'.txt'),'w') as f:
        for l in log: f.write(l)

# Testing
def test():
    objects, names, backgrounds = initialize(backgrounds_dir="backgrounds", classes_dir="crops")
    mkimage('train', objects, names, backgrounds, output_dir="images_out", maxobjs=6)
