#!/usr/bin/env python3
"""
Copyright (C) 2021 P Smit
Copyright (C) 2018 FireEye, Inc., created by Andrew Shay. All Rights Reserved.
"""

import PIL

from PIL import Image, ImageDraw
import math
import os
import glob
import argparse

def parseArgs():
    p = argparse.ArgumentParser(description='Draw some gauges.',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('percentages', metavar='N%', type=int, nargs='*',
                        default=list(range(0, 101, 10)),
                        help='percentages to draw the needle at')
    p.add_argument('--thumbnails', action='store_true',
                        help='generate thumbnails')
    p.add_argument('--gaugeDegrees', metavar="N°", type=int, default=180+90,
                    help="degrees the needle spans on gauge, assumed to be symetric around North.")
    p.add_argument('--debug', action='store_true',
                        help='print debug messages.')
    #Note: use vars(p.parse_args()) to turn into dict
    return p.parse_args()


args = parseArgs()
debug = args.debug
if debug: print(f"Debug: {args=}")

# percentages = [ 0, 25, 50, 75, 100 ]  # Percent for gauge
percentages = args.percentages

output_file_name_template = 'new_gauge{extra}{percent}%.png'
fileList = glob.glob(output_file_name_template.format(extra="_", percent="*"))
for filePath in fileList: os.remove(filePath)

fnImgNeedle = 'needle-red.png'
locNeedleRotate = (510, 480)
NeedleResizeFactor = 0.28

fnImgGauge = 'gauge-md.png'
locGaugePlaceNeedle = (150, 145)

locCalcPlaceNeedle = (
        locGaugePlaceNeedle[0] - math.trunc(locNeedleRotate[0] * NeedleResizeFactor) ,
        locGaugePlaceNeedle[1] - math.trunc(locNeedleRotate[1] * NeedleResizeFactor)
    )

for percent in percentages:
    fraction = percent / 100
    gaugeDegrees = args.gaugeDegrees
    rotation = ( gaugeDegrees ) * fraction  # 180 degrees because the gauge is half a circle
    rotation = gaugeDegrees / 2 - rotation  # Factor in the needle graphic pointing to 50 (90 degrees)

    dial = Image.open(fnImgNeedle)
    #  ,expand=True not working well, better to create needle canvas big enough for needle to fit in all directions after rotation.
    dial = dial.rotate(rotation, resample=PIL.Image.BICUBIC, center=locNeedleRotate)  # Rotate needle
    dial = dial.resize( (math.trunc(dial.size[0]*NeedleResizeFactor), math.trunc(dial.size[1]*NeedleResizeFactor) ) )
    if debug: dial.save(f"needle-rotate-{percent}.png")

    gauge = Image.open(fnImgGauge)



    if debug: print(f"Debug {[item1 + item2 for item1, item2 in zip(locGaugePlaceNeedle, locNeedleRotate)]} {fnImgNeedle}:{dial.size} {fnImgGauge}:{gauge.size} place:{locCalcPlaceNeedle} rotation:{rotation}")
    gauge.paste(dial, locCalcPlaceNeedle, mask=dial)  # Paste needle onto gauge

    gaugeDraw = ImageDraw.Draw(gauge)
    if debug: print(f"DEBUG:: {locGaugePlaceNeedle[0]-50}, {locGaugePlaceNeedle[0]+200}")
    gaugeDraw.text((locGaugePlaceNeedle[0]-10, locGaugePlaceNeedle[0]+120), f"%{percent}", outline='red', fill='blue')

    if args.thumbnails:
        MAX_SIZE = (30, 30)
        gauge.thumbnail(MAX_SIZE)
        fn=output_file_name_template.format(extra="_thumb_", percent=percent)
        gauge.save()
    else:
        fn=output_file_name_template.format(extra="_", percent=percent)
        gauge.save(fn)
    print(f"Created: {fn}")
