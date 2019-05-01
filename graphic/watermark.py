# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    Author Thiago Druciaki <druciaki@gmail.com>
#
#    This uses Pillow lib to put a watermark on another image or in all images on a given directory
#    usage: python watermark.py <watermark image file> <Image or Image Directory> <watermark position> 
#
#    Python 3.5.2
#
##############################################################################

from PIL import Image
import sys, os


FILE_IMAGE_EXTENSIONS = ['png','jpg']   # extensions considered when passing directory
WATERMARK_INTENSITY = 125               # Alpha: 0-255
WATERMARK_FILE_PREFIX = 'wm_'           # prefix of files being created
POSITION = 1
FILES = []

def get_watermark_position(imgsize, wmsize, position):
    x = 0
    y = 0
    if position in [3, 6, 9]:
        x = imgsize[0] - wmsize[0]
    elif position in [2, 5, 8]:
        x = int(imgsize[0]/2) - int(wmsize[0]/2)
    if position in [4, 5, 6]:
        y = int(imgsize[1]/2) - int(wmsize[1]/2)
    elif position in [7, 8, 9]:
        y = imgsize[1] - wmsize[1]
    return (x,y)


def apply_watermark(watermark, image_file, position):
    img = Image.open(image_file)
    img = img.convert('RGBA')
    mask = Image.new('RGBA', img.size, (0,0,0,0))
    xy = get_watermark_position(img.size, watermark.size, position)
    mask.paste(watermark, xy)
    result = Image.alpha_composite(img,mask)
    output_name = image_file[:-3]+"png"
    if(len(image_file.split('/'))>1): # workaround to ignore directories
        dirindex = output_name.rfind('/')+1
        output_name = output_name[:dirindex] + WATERMARK_FILE_PREFIX + output_name[dirindex:]
    else:
        output_name = WATERMARK_FILE_PREFIX+output_name
    print("Saving "+output_name)
    result.save(output_name)


def help():
    print ("python watermark.py <watermark image.png> <ANOTHER_FILE.png or directory path> <position (optional)>")
    print ("Position values:")
    print (" _______")
    print ("|1--2--3|")
    print ("|4--5--6|")
    print ("|7--8--9|")
    exit()

if len(sys.argv) < 3 or len(sys.argv) > 4:
    help()

if len(sys.argv) == 4:
    try:
        POSITION = int(sys.argv[3])
    except:
        help()

if os.path.isfile(sys.argv[2]):
    FILES.append(sys.argv[2])
elif os.path.isdir(sys.argv[2]):
    folder = sys.argv[2]
    for file_name in os.listdir(sys.argv[2]):
        if file_name[-3:] in FILE_IMAGE_EXTENSIONS:
            FILES.append(folder + file_name)
else:
    exit()

watermark = Image.open(sys.argv[1])
watermark.convert('RGBA')
watermark.putalpha(WATERMARK_INTENSITY)
for image_path in FILES:
    apply_watermark(watermark, image_path, POSITION)

