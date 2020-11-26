#!/usr/bin/env python

from gimpfu import *

RED = 0
GREEN = 1
BLUE = 2
ALPHA = 3
CHANNELS = 4

def highlight_transparent(image):
    pdb.gimp_image_undo_group_start(image)
    width, height = image.width, image.height
    selection = image.selection.get_pixel_rgn(0, 0, width, height)
    for layer in image.layers:
        if layer.name == 'Transparency Filter':
            image.remove_layer(layer)
    reference_layer = image.active_layer
    image.add_layer(pdb.gimp_layer_new(image, width, height, 1, 'Transparency Filter', 100, 0), 0)
    transparecy_filter = image.layers[0]
    pr = reference_layer.get_pixel_rgn(0, 0, width, height, False, False)
    prt = transparecy_filter.get_pixel_rgn(0, 0, width, height, False, False)
    for i in range(0, width):
        for j in range(0, height):
            if selection[i, j] == '\xff':
                pixel = pr[i, j]
                not_solid = str(pixel[ALPHA]) != '\xff'
                transparent = str(pixel[ALPHA]) == '\x00'
                has_color = str(pixel[RED]) != '\x00' or str(pixel[GREEN]) != '\x00' or str(pixel[BLUE]) != '\x00'
                if not_solid and not transparent:
                    prt[i, j] = '\xff\x00\x00\x80'
                if transparent and not has_color:
                    prt[i, j] = '\x00\xff\x00\x80'
                if transparent and has_color:
                    prt[i, j] = '\xff\x00\xff\x80'
                    pr[i, j] = '\x00\x00\x00\x00'
    transparecy_filter.flush()
    reference_layer.flush()
    ##transparecy_filter.update(0, 0, width, height)
    pdb.gimp_image_undo_group_end(image)


register(
    "python-fu-identify-transparency",
    "Highlights transparent pixels",
    "Creates a new transparent layer highlighting transparent pixels",
    "Miguel Maldonado", "kelifire", "2020",
    "Highlight Transparent...",
    "RGBA",
    [
        (PF_IMAGE, "image", "takes current image", None),
    ],
    [],
    highlight_transparent, menu="<Image>/Filters/Enhance")

main()
