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
#    Making white pixels transparent
#    usage: python white2transparent.py <img>
#
#    Python 3.5.2
#
##############################################################################

from PIL import Image
import sys

img = Image.open(sys.argv[1])
TRANSPARENT = (255,255,255,0)

def is_white(pixel):
    if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
        return True
    return False

if img.mode != 'RGBA':
    img = img.convert('RGBA')

xl,yl = img.size
for x in range(0,xl):
    for y in range(0,yl):
        if is_white( img.getpixel( (x,y) )):
            img.putpixel((x,y), TRANSPARENT)

img.save("T"+sys.argv[1][:-3]+"png")

