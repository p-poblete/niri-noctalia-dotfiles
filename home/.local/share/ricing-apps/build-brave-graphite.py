#!/usr/bin/env python3
"""Generate the fixed Liquid Clear Graphite browser theme."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

root = Path.home()/'.local/share/noctalia/brave-theme'
images = root/'images'
images.mkdir(parents=True,exist_ok=True)


def plate(name,top,bottom,strength=1.0):
    w,h=2048,192
    gradient=Image.new('RGB',(1,h))
    gradient.putdata([tuple(round(a+(b-a)*y/(h-1)) for a,b in zip(top,bottom)) for y in range(h)])
    result=gradient.resize((w,h))
    shine=Image.new('RGBA',(w,h)); d=ImageDraw.Draw(shine)
    d.ellipse((-350,-175,1200,55),fill=(225,237,255,round(45*strength)))
    d.ellipse((700,-190,2400,35),fill=(255,255,255,round(18*strength)))
    shine=shine.filter(ImageFilter.GaussianBlur(24))
    result=Image.alpha_composite(result.convert('RGBA'),shine)
    d=ImageDraw.Draw(result)
    d.line((0,0,w,0),fill=(220,231,248,round(70*strength)))
    d.line((0,h-1,w,h-1),fill=(4,6,10,90))
    result.convert('RGB').save(images/name)


plate('graphite-frame.png',(50,55,65),(23,26,32))
plate('graphite-frame-inactive.png',(39,43,51),(22,25,30),.55)
plate('graphite-toolbar.png',(66,72,83),(38,43,52),.8)
plate('graphite-tabs.png',(37,41,49),(24,27,33),.4)
bg=Image.new('RGB',(1920,1080),(20,23,29))
glow=Image.new('RGBA',bg.size); d=ImageDraw.Draw(glow)
d.ellipse((150,-350,1750,450),fill=(156,173,200,20))
bg=Image.alpha_composite(bg.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(150)))
bg.convert('RGB').save(images/'graphite-newtab.png')
colors={
 'frame':[27,30,36], 'frame_inactive':[24,27,32],
 'frame_incognito':[24,27,33], 'frame_incognito_inactive':[22,25,30],
 'toolbar':[48,53,63], 'toolbar_text':[239,243,249],
 'toolbar_button_icon':[223,231,243], 'tab_text':[248,250,255],
 'tab_background_text':[184,195,211], 'tab_background_text_inactive':[150,161,178],
 'bookmark_text':[226,233,244], 'omnibox_background':[29,33,41],
 'omnibox_text':[242,246,252], 'ntp_background':[20,23,29],
 'ntp_text':[229,236,247], 'ntp_link':[206,220,240],
 'ntp_header':[43,49,59], 'button_background':[61,68,80],
}
manifest={
 'manifest_version':3,'name':'Liquid Clear Graphite','version':'2.0.0',
 'description':'Tema fijo de grafito y plata, con reflejos suaves. Sin permisos ni scripts.',
 'theme':{
  'colors':colors,
  'images':{'theme_frame':'images/graphite-frame.png',
            'theme_frame_inactive':'images/graphite-frame-inactive.png',
            'theme_frame_incognito':'images/graphite-frame-inactive.png',
            'theme_toolbar':'images/graphite-toolbar.png',
            'theme_tab_background':'images/graphite-tabs.png',
            'theme_ntp_background':'images/graphite-newtab.png'},
  'tints':{'buttons':[-1,-1,-1],'frame':[-1,-1,-1],
           'frame_inactive':[-1,-1,-1],'frame_incognito':[-1,-1,-1]},
  'properties':{'ntp_background_alignment':'top','ntp_background_repeat':'no-repeat',
                'ntp_logo_alternate':1},
 }
}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Tema creado:',root)
