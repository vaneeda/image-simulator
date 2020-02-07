import sys
import argparse
from generate import mkimage, initialize
import csv
import glob
import os
# check if python3 is used
if sys.version_info < (3, 0):
    print("This programs need python3x to run. Aborting.")
    sys.exit(1)

p = argparse.ArgumentParser(description='Generate images from background and elements.')
p.add_argument('-d', '--path_to_directory'
               , help='path_to_directory containing backgrounds and crops folder')
p.add_argument('-b', '--backgrounds', default = 'backgrounds'
               , help='name of directory containing background images')
p.add_argument('-c', '--classes', default = 'crops'
               , help='directory containing element images, one subdirectory per class')
p.add_argument('-s', '--single', action='store_true'
               , help='generate images containing one class elements only')
p.add_argument('-n'
               , help='number of images to generate')
p.add_argument('-e', default = 6
               , help='max number of elements per image')
p.add_argument('-o'
               , help='directory to store generated images')

args = p.parse_args()

backgrounds_dir = os.path.join(args.path_to_directory, args.backgrounds)
classes_dir = os.path.join(args.path_to_directory, args.classes)
objects, names, backgrounds = initialize(backgrounds_dir, classes_dir)
n = int(args.n)

output_dir = os.path.join(args.path_to_directory, args.o)

for i in range(1,int(n)+1):
    mkimage(args.o+'_%d' % int(i), objects, names, backgrounds,
            output_dir=output_dir, maxobjs=args.e, single=args.single)

filename = args.o + "_annotations.csv"

txt_files = os.path.join(output_dir, '*.txt')

# Convert txt files to one csv annotation file
with open(os.path.join(args.path_to_directory, filename), 'w') as output_file:
    for txt_file in glob.glob(txt_files):
        with open(txt_file, "r") as input_file:
            in_txt = csv.reader(input_file, delimiter=',')
            out_csv = csv.writer(output_file, delimiter=',')
            out_csv.writerows(in_txt)