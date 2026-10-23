#!/usr/bin/env python3
"""Neutral graphite new-tab wallpaper matching Liquid Clear Graphite."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

size=(2560,1600)
top,bottom=(37,45,57),(20,23,29)
base=Image.new('RGB',(1,size[1]))
base.putdata([tuple(round(a+(b-a)*y/(size[1]-1)) for a,b in zip(top,bottom)) for y in range(size[1])])
base=base.resize(size).convert('RGBA')
glow=Image.new('RGBA',size)
d=ImageDraw.Draw(glow)
d.ellipse((-400,-1200,2960,700),fill=(191,205,224,27))
glow=glow.filter(ImageFilter.GaussianBlur(260))
result=Image.alpha_composite(base,glow).convert('RGB')
output=Path.home()/'Imágenes/Brave-Liquid-Graphite.png'
result.save(output)
print(output)
