#!/usr/bin/env python

import os, sys, glob
# import shutil
from PIL import Image

#os.system('blender -b boss_chest.blend --python-text RenderAll')

tile_w = 192
tile_h = 384
tile_floor_h = int(tile_h/4)
tile_floor_offset = int(tile_h * 0.75)
tile_short_offset = int(tile_h * 0.5)
tile_floor_center_h = int(tile_h * 0.875)
tile_large_offset_step = int(tile_h * 0.125)

output_path = sys.path[0] + "/output/"

mod_path = output_path + "../../../mod_data/core/"
mod_image_path = "images/tilesets/"
mod_tilesetdef_path = "tilesetdefs/"

os.makedirs(mod_path, exist_ok=True)
os.makedirs(mod_path + mod_image_path, exist_ok=True)
os.makedirs(mod_path + mod_tilesetdef_path, exist_ok=True)

tiled_path = output_path + "../../../../tiled/tilesheets/"
os.makedirs(tiled_path, exist_ok=True)

# tileset_cols = 16
# tileset_rows = 20

tile_defs = []
anim_defs = {}
blank_tiles = []

# create blank sheet images. The first one is a single sheet with everything on it for Flare. The others are split for usage in Tiled.
tile_sheet_tiled_filename = tiled_path + "boss_chest.png"
print("Writing tile sheet file: " + tile_sheet_tiled_filename)
tile_sheet_tiled = Image.new('RGBA', (tile_w * 4, int(tile_h / 2)))

tile_filenames = sorted(glob.glob(output_path + "boss_chest/*.png"))

# boss chest
target_x = 0
target_y = 0
tile_id = 288

tile_filenames = sorted(glob.glob(output_path + "boss_chest/*.png"))

for i in range(0, len(tile_filenames)):
    if tile_id not in blank_tiles:
        tile = Image.open(tile_filenames[i])

        tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * 4):
        target_x = 0
        target_y += tile_h


# save the tilesheet files
tile_sheet_tiled.save(tile_sheet_tiled_filename)

