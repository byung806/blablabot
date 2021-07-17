import os
import numpy as np
from PIL import Image

MC_MAPPING = {}
mc_mapping = {}

def has_transparent(img):
    data = img.getdata()
    for item in data:
        if item[3] == 0:
            return True
    return False

def average(img):
    r, g, b, a = 0, 0, 0, 0
    # a is the solid amount, NOT the transparency amount
    solid_count = 0
    data = img.getdata()
    for item in data:
        r += item[0] * item[3] / 255
        g += item[1] * item[3] / 255
        b += item[2] * item[3] / 255
        a += (255 - item[3]) / 255
        solid_count += item[3] / 255
    return (r/solid_count, g/solid_count, b/solid_count, solid_count/(a+solid_count))

#rewrite so it accepts rgba and it gets average for r, g, b, and also a as well

for name in os.listdir(r'C:\Users\byung\PycharmProjects\DiscordBot\cogs\utilityCommands\solid_blocks'):
    if name != 'aa_SOLIDBLOCKS_rgb_maker.py' and name != 'aa_mc_mapping.py':
        if name.endswith('.mcmeta'):
            os.remove(name)
            print('Removed', name)
        elif name.endswith('.png'): #and name == 'attached_melon_stem.png':
            img = Image.open(name).convert('RGBA')

            if Image.open(name).size != (16,16):
                img.crop((0, 0, 16, 16)).save(name)
                print('Cropped', name)
            if name != 'air.png':
                avg_color = average(img)
                avg = list(map(round, avg_color[0:3]))
                avg.append(avg_color[-1])
            else:
                avg = (0, 0, 0, .0)
            print('Generated color for', name, f'({avg})')
            MC_MAPPING[tuple(avg)] = name
print(MC_MAPPING)
# snow 249, 254, 254, 1.0
# white stained glass 255, 255, 255, 0.46012561274509944