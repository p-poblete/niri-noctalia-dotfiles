#!/usr/bin/env python3
"""Build a user-owned Mint-Y variant from the exact Noctalia accent colors."""
import fcntl
import json
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageOps
from glass_material import render

ROOT = Path(__file__).resolve().parent
SOURCE = Path('/usr/share/icons/Mint-Y')
ICONS = Path.home() / '.local/share/icons'
NAME = 'Mint-Y-Liquid-Clear-v1'
TARGET = ICONS / NAME
SVG = 'http://www.w3.org/2000/svg'


def build(palette):
    palette = {key: palette[key] for key in ('primary', 'on_primary')}
    for key in ('primary', 'on_primary'):
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', palette[key]):
            raise ValueError('Invalid palette color')
    stamp = json.dumps(palette, sort_keys=True)
    if (TARGET / 'noctalia-palette.json').exists():
        if (TARGET / 'noctalia-palette.json').read_text() == stamp:
            print('Icon palette unchanged')
            return
    stage = ICONS / (NAME + '.building')
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    count = 0
    for current, dirs, files in os.walk(SOURCE, followlinks=False):
        rel = Path(current).relative_to(SOURCE)
        destdir = stage / rel
        destdir.mkdir(parents=True, exist_ok=True)
        for name in list(dirs):
            src = Path(current) / name
            if src.is_symlink():
                (destdir / name).symlink_to(src.resolve(), target_is_directory=True)
                dirs.remove(name)
        for name in files:
            src, dst = Path(current) / name, destdir / name
            if name in ('index.theme', 'icon-theme.cache'):
                continue
            if src.is_symlink():
                resolved = src.resolve()
                if resolved.is_relative_to(SOURCE):
                    newtarget = stage / resolved.relative_to(SOURCE)
                    dst.symlink_to(os.path.relpath(newtarget, dst.parent))
                else:
                    dst.symlink_to(resolved)
            elif 'symbolic' in str(rel) or '-symbolic.' in name:
                # GTK recolors symbolic icons itself using the UI foreground.
                dst.symlink_to(src)
            elif src.suffix == '.png':
                with Image.open(src) as original:
                    tinted = render(original)
                    tinted.save(dst, compress_level=1)
                count += 1
            elif src.suffix == '.svg':
                tree = ET.parse(src)
                root = tree.getroot()
                definitions = ET.Element(f'{{{SVG}}}defs')
                effect = ET.SubElement(definitions, f'{{{SVG}}}filter', {
                    'id': 'noctalia-accent', 'color-interpolation-filters': 'sRGB',
                    'x': '0', 'y': '0', 'width': '1', 'height': '1'})
                low = tuple(int(palette['on_primary'][i:i+2],16)/255 for i in (1,3,5))
                high = tuple(int(palette['primary'][i:i+2],16)/255 for i in (1,3,5))
                values = []
                for a,b in zip(low, high):
                    values.extend([(b-a)*.2126,(b-a)*.7152,(b-a)*.0722,0,a])
                values.extend([0,0,0,0.35,0])
                ET.SubElement(effect, f'{{{SVG}}}feColorMatrix', {
                    'type':'matrix','values':' '.join(str(x) for x in values)})
                group = ET.Element(f'{{{SVG}}}g', {'filter':'url(#noctalia-accent)'})
                for child in list(root):
                    if child.tag.split('}')[-1] not in ('defs','metadata','title','desc','style'):
                        root.remove(child)
                        group.append(child)
                root.insert(0, definitions)
                root.append(group)
                tree.write(dst, encoding='utf-8', xml_declaration=True)
                count += 1
            else:
                dst.symlink_to(src)
    index = (SOURCE/'index.theme').read_text()
    index = index.replace('Name=Mint-Y\n', f'Name={NAME}\n', 1)
    index = re.sub(r'^Inherits=.*$', 'Inherits=Mint-Y,Adwaita,hicolor', index, flags=re.M)
    (stage/'index.theme').write_text(index)
    (stage/'noctalia-palette.json').write_text(stamp)
    shutil.copy2('/usr/share/doc/mint-y-icons/copyright', stage/'COPYRIGHT')
    subprocess.run(['gtk-update-icon-cache','-f','-t',str(stage)],check=True,capture_output=True)
    previous = ICONS/(NAME+'.previous')
    if previous.exists():
        shutil.rmtree(previous)
    if TARGET.exists():
        TARGET.rename(previous)
    stage.rename(TARGET)
    if previous.exists():
        shutil.rmtree(previous)
    print(f'Generated {count} tinted icons: {palette["primary"]}')



if __name__ == '__main__':
    with (ROOT/'sync.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        build({'primary':'#ffffff','on_primary':'#a9bfd1'})
