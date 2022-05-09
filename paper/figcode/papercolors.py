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