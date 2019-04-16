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
#    This uses Pillow lib to mix two images in a "chessboard" way
#    usage: python pypicmix.py <Image File 1> <Image File 2> <block size (pixels)> 
#
##############################################################################

from PIL import Image
import sys

FILES = []
BOX_SIZE = 10

try:
    FILES = (sys.argv[1],sys.argv[2])
except IndexError:
    print "python pypicmix.py <FILE.png> <ANOTHER_FILE.png> <block size (optional)>"
try:
    BOX_SIZE = int(sys.argv[3])
except:
    pass

img = Image.open(FILES[0])
img2 = Image.open(FILES[1])

# Verify sizes and stretch the second image to fit if necessary
if img.size != img2.size:
    img2 = img2.resize(img.size, Image.LANCZOS)

mask = Image.new('1', img.size, color=0)
new_img = Image.new(img.mode, img.size, color=0)

yc = 0
xc = 0
current_color = 0
last_line_color = None

def switch_color_bw(c):
    if c:
        return 0
    return 1

for y in range(0,mask.size[1]):
    last_line_color = current_color
    if yc < BOX_SIZE:
        current_color = last_line_color
    else:
        current_color = switch_color_bw(current_color)
        yc = 0


    for x in range(0,mask.size[0]):
        if xc<BOX_SIZE:
            mask.putpixel((x,y), current_color)
        else:
            current_color = switch_color_bw(current_color)
            mask.putpixel((x,y), current_color)
            xc = 0
            continue
        xc+=1
    yc +=1
    xc = 0
    last_line_color = current_color

# Apply the "chess" mask generated
for y in range(0,mask.size[1]):
    for x in range(0,mask.size[0]):
        if mask.getpixel((x,y)):
            new_img.putpixel((x,y), img.getpixel((x,y)))
        else:
            new_img.putpixel((x,y), img2.getpixel((x,y)))

new_img.save('output.png')
print "output.png generated"

