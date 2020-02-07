import sys
# check if python3 is used
if sys.version_info < (3, 0):
    print("This programs need python3x to run. Aborting.")
    sys.exit(1)

import os
import random
from PIL import Image
from math import floor, sqrt

dict = {"mackerel": 35/35, "bluewhiting": 27/35, "herring": 33/35, "krill": 1/35, "lanternfish": 9/35}

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
    cls0 = random.randint(0,len(objs)-1)   # Selects random class

    num_obj= random.randint(1, maxobjs)   # Randomly chooses a number of objects (max no defined by user)
    scale_list= [i/100 for i in random.sample(range(80,200), num_obj)]
    scale_list.sort()

    for c in range(0, num_obj):

        if single: cls=cls0
        else: cls = random.randint(0,len(objs)-1)
        obj = random.choice(objs[cls]) #Selects a random object from the selected class
        # random modifications
        flipLR, flipTB = random.randint(0, 3), random.randint(0, 10)  # random flip
        if (flipLR == 0):
            obj = obj.transpose(Image.FLIP_LEFT_RIGHT)
        if (flipTB == 0):
            obj = obj.transpose(Image.FLIP_TOP_BOTTOM)
        norm = sqrt(obj.size[0]*obj.size[1])
        obj  = obj.resize([int(dict[names[cls]]*s*scale_list[c]*300/norm) for s in obj.size],
                          Image.ANTIALIAS)
        obj  = obj.rotate(random.gauss(0,8), expand=1, resample=Image.NEAREST)
        imx,imy = im.size
        posx = random.randint(-floor(3*obj.size[0]/4),imx-floor(obj.size[0]/4))
        posy = random.randint(-floor(3*obj.size[1]/4),imy-floor(obj.size[1]/4))
        im.paste(obj,(posx,posy),obj)
        path_to_image = os.path.join(output_dir, filename + '.png')
        log = log + ['{},{},{},{},{},{}\n'.format(path_to_image,
                                                  max(0, posx),
                                                  max(0, posy),
                                                  min(posx + obj.size[0], imx),
                                                  min(posy + obj.size[1], imy),
                                                  names[cls])]

    im.save(os.path.join(output_dir,filename+'.png'))
    with open(os.path.join(output_dir,filename+'.txt'),'w') as f:
        for l in log: f.write(l)

# Testing
def test():
    objects, names, backgrounds = initialize(backgrounds_dir="backgrounds", classes_dir="crops")
    mkimage('train', objects, names, backgrounds, output_dir="images_out", maxobjs=6)
