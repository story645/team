import re

sub = re.compile(r"\\definecolor\{(?P<name>.*)\}\{HTML\}\{(?P<color>.*)\}")

def build_colors(filepath = '../notation.sty'):
    colordict = {}
    with open(filepath) as f:
        for line in f.readlines():
            if groups := sub.match(line):
                colordict[groups.group('name')] = "#"+ groups.group('color')
    return colordict

colordict = build_colors()

def lighten(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])