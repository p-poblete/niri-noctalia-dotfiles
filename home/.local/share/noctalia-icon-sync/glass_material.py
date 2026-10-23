"""Static clear-glass material: transparent body, bevel, relief and highlights."""
from functools import lru_cache
from PIL import Image, ImageChops, ImageFilter, ImageOps


def layer(color, alpha):
    result = Image.new('RGBA', alpha.size, (*color, 0))
    result.putalpha(alpha)
    return result


@lru_cache(maxsize=24)
def lighting(size):
    w, h = size
    shine = Image.new('L', size)
    # A broad upper reflection and a narrow diagonal glint, never an opaque tile.
    shine.putdata([
        round(12 + 62 * max(0, 1-y/max(h-1,1))**4
              + 34 * max(0, 1-abs(x/max(w-1,1)+y/max(h-1,1)-0.55)/0.18))
        for y in range(h) for x in range(w)
    ])
    return shine


def render(original):
    image = original.convert('RGBA')
    alpha = image.getchannel('A')
    rgb = image.convert('RGB')
    sample = image.copy()
    sample.thumbnail((32, 32))
    colors = sample.getcolors(1024) or []
    opaque = [(count, color) for count, color in colors if color[3] > 220]
    background = max(opaque, default=(1,(128,128,128,255)))[1][:3]
    distance = ImageChops.difference(rgb, Image.new('RGB', image.size, background))
    red, green, blue = distance.split()
    distance = ImageChops.lighter(ImageChops.lighter(red,green),blue)
    glyph = distance.point(lambda v: min(235, max(0, (v-24)*3)))
    # Keep glyphs separate from the bevel, even when source shapes touch the edge.
    inner = alpha.filter(ImageFilter.MinFilter(3))
    glyph = ImageChops.multiply(glyph, inner)
    glyph = glyph.point(lambda v: round(v*.65))
    radius = max(.35, min(image.size)/120)
    erosion = alpha.filter(ImageFilter.MinFilter(3))
    rim = ImageChops.subtract(alpha,erosion)
    rim = rim.filter(ImageFilter.GaussianBlur(radius))
    body = ImageChops.multiply(alpha,lighting(image.size))
    result = layer((228,239,255),body)
    # Dark engraving followed by the bright symbol gives separation on light backgrounds.
    engraved = ImageChops.offset(glyph, 0, max(1, image.height//96))
    result = Image.alpha_composite(result,layer((18,25,38),engraved.point(lambda v: round(v*.55))))
    result = Image.alpha_composite(result,layer((250,253,255),glyph))
    result = Image.alpha_composite(result,layer((255,255,255),rim.point(lambda v: min(230,round(v*1.8)))))
    return result
