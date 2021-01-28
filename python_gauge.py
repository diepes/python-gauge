"""
Copyright (C) 2018 FireEye, Inc., created by Andrew Shay. All Rights Reserved.
"""

import PIL

from PIL import Image, ImageDraw
import math
import os
import glob

debug = False

# percentages = [ 0, 25, 50, 75, 100 ]  # Percent for gauge
percentages = range(0, 101, 10)

output_file_name_template = 'new_gauge_{percent}%.png'
fileList = glob.glob(output_file_name_template.format(percent="*"))
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
    gaugeDegrees = 180 + 90
    rotation = ( gaugeDegrees ) * fraction  # 180 degrees because the gauge is half a circle
    rotation = gaugeDegrees / 2 - rotation  # Factor in the needle graphic pointing to 50 (90 degrees)

    dial = Image.open(fnImgNeedle)
    #  ,expand=True not working well, better to create needle canvas big enough for needle to fit in all directions after rotation.
    dial = dial.rotate(rotation, resample=PIL.Image.BICUBIC, center=locNeedleRotate)  # Rotate needle
    dial = dial.resize( (math.trunc(dial.size[0]*NeedleResizeFactor), math.trunc(dial.size[1]*NeedleResizeFactor) ) )
    if debug: dial.save(f"needle-rotate-{percent}.png")

    gauge = Image.open(fnImgGauge)



    print(f"Debug {[item1 + item2 for item1, item2 in zip(locGaugePlaceNeedle, locNeedleRotate)]} {fnImgNeedle}:{dial.size} {fnImgGauge}:{gauge.size} place:{locCalcPlaceNeedle} rotation:{rotation}")
    gauge.paste(dial, locCalcPlaceNeedle, mask=dial)  # Paste needle onto gauge

    gaugeDraw = ImageDraw.Draw(gauge)
    print(f"DEBUG:: {locGaugePlaceNeedle[0]-50}, {locGaugePlaceNeedle[0]+200}")
    gaugeDraw.text((locGaugePlaceNeedle[0]-10, locGaugePlaceNeedle[0]+120), f"%{percent}", outline='red', fill='blue')

    gauge.save(output_file_name_template.format(percent=percent))
