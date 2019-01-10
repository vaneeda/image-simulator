import sys
import argparse
from generate import mkimage, initialize

# check if python3 is used
if sys.version_info < (3, 0):
    print("This programs need python3x to run. Aborting.")
    sys.exit(1)

p = argparse.ArgumentParser(description='Generate images from background and elements.')
p.add_argument('-b', '--backgrounds'
               , help='directory containing background images')
p.add_argument('-c', '--classes'
               , help='directory containing element images, one subdirectory per class')
p.add_argument('-s', '--single', action='store_true'
               , help='generate images containing one class elements only')
p.add_argument('-n'
               , help='number of images to generate')
p.add_argument('-e'
               , help='max number of elements per image')
p.add_argument('-o'
               , help='directory to store generated images')

args = p.parse_args()
print(args)

objects, names, backgrounds = initialize(backgrounds_dir=args.backgrounds, classes_dir=args.classes)

n = int(args.n)

if args.e == None: e=6
else: e=int(args.e)

for i in range(1,int(n)+1):
    mkimage('test_%d' % int(i), objects, names, backgrounds, output_dir=args.o, maxobjs=e, single=args.single)

    
