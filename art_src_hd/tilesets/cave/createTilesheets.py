#!/usr/bin/env python

import os, sys, glob
import shutil
from PIL import Image

tile_w = 192
tile_h = 384
tile_floor_h = int(tile_h/4)
# tile_w = 64
# tile_h = 128
tile_floor_offset = int(tile_h * 0.75)
tile_short_offset = int(tile_h * 0.5)
tile_floor_center_h = int(tile_h * 0.875)
tile_large_offset_step = int(tile_h * 0.125)
tile_small_object_offset = int(tile_h * 0.375)

output_path = sys.path[0] + "/output/"

mod_path = output_path + "../../../mod_data/core/"
mod_image_path = "images/tilesets/"
mod_tilesetdef_path = "tilesetdefs/"

os.makedirs(mod_path, exist_ok=True)
os.makedirs(mod_path + mod_image_path, exist_ok=True)
os.makedirs(mod_path + mod_tilesetdef_path, exist_ok=True)

tiled_path = output_path + "../../../../tiled/tilesheets/"
os.makedirs(tiled_path, exist_ok=True)

tileset_cols = 16
tileset_rows = 19
tileset_tiled_rows = tileset_rows - 4 # two rows of water animations; one row for teleporter; one row for boss chest

tile_defs = []
anim_defs = {}
blank_tiles = []

# create blank sheet images. The first one is a single sheet with everything on it for Flare. The others are split for usage in Tiled.
tile_sheet_filename = mod_path + mod_image_path + "tileset_cave.png"
print("Writing tile sheet file: " + tile_sheet_filename)
tile_sheet = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_rows))

tile_sheet_tiled_filename = tiled_path + "cave.png"
print("Writing tile sheet file: " + tile_sheet_tiled_filename)
tile_sheet_tiled = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_tiled_rows))

tile_sheet_tiled_2x2_filename = tiled_path + "cave_2x2.png"
print("Writing tile sheet file: " + tile_sheet_tiled_2x2_filename)
tile_sheet_tiled_2x2 = Image.new('RGBA', ((tile_w * 2) * 2, int(tile_h / 2)))

# floors
tile_filenames = sorted(glob.glob(output_path + "floor/*.png"))
target_x = 0
target_y = 0

# first tile id is offset by one row (for collision tiles)
tile_id = tileset_cols

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# minecart tracks
tile_filenames = sorted(glob.glob(output_path + "floor_tracks/*.png"))
target_x = 0
target_y = tile_h
tile_id = tileset_cols * 2

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# floor decor
tile_filenames = sorted(glob.glob(output_path + "floor_decor/*.png"))
target_x = 0
target_y = tile_h * 2
tile_id = tileset_cols * 3

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# floors "corner" tiles
corner_floor_tile_img = Image.open(output_path + "floor/0001.png")
target_x = tile_w * 8
target_y = tile_h * 2
tile_id = (tileset_cols * 3) + 8

corner_floor_blank_w = int(tile_w * 0.40625)
corner_floor_crop_w = tile_w - corner_floor_blank_w
corner_floor_crop_x = [corner_floor_blank_w, 0]

for i in range(0, len(corner_floor_crop_x)):
    tile = corner_floor_tile_img.crop((corner_floor_crop_x[i], 0, corner_floor_crop_x[i] + corner_floor_crop_w, tile_floor_h))

    tile_sheet.alpha_composite(tile, (target_x + corner_floor_crop_x[i], target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x + corner_floor_crop_x[i], target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# walls
target_x = 0
target_y = tile_h * 3
tile_id = tileset_cols * 4

tile_filenames = sorted(glob.glob(output_path + "walls/*.png"))

walls_remapped = {
    24: 32,
    25: 33,
    26: 36,
    27: 37,
    28: 34,
    29: 38,
    30: 52,
    31: 35,
    32: 53,
    33: 54,
    34: 39,
    35: 55,
}
for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i>= 24 and i in walls_remapped:
        tile_id = (tileset_cols * 4) + walls_remapped[i]
        target_x = int(tile_id % tileset_cols) * tile_w
        target_y = (int(tile_id / tileset_cols) * tile_h) -  tile_h

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# mine walls
target_x = tile_w * 8
target_y = tile_h * 5
tile_id = (tileset_cols * 6) + 8

tile_filenames = sorted(glob.glob(output_path + "walls_mine/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# mushrooms
target_x = 0
target_y = tile_h * 6
tile_id = tileset_cols * 7

tile_filenames = sorted(glob.glob(output_path + "mushrooms/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i == 4:
        # mushroom floor tiles are on the next row, target_x lines up
        target_y += tile_h
        tile_id += tileset_cols
    elif i == 8:
        # corner walls are back on the previous row, target_x lines up still
        target_y -= tile_h
        tile_id -= tileset_cols

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# exit walls
# NOTE EXPERIMENTAL
# target_x = tile_w * 8
# target_y = tile_h * 4
# tile_id = (tileset_cols * 5) + 8
#
# tile_filenames = sorted(glob.glob(output_path + "exits/*.png"))
#
# for i in range(0, len(tile_filenames)):
#     tile = Image.open(tile_filenames[i])
#
#     if i == 8:
#         target_x = tile_w * 12
#         target_y = tile_h * 6
#         tile_id = (tileset_cols * 7) + 12
#
#     tile_sheet.alpha_composite(tile, (target_x, target_y))
#     tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))
#
#     if tile_id not in blank_tiles:
#         tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))
#
#     tile_id += 1
#     target_x += tile_w
#     if target_x >= (tile_w * tileset_cols):
#         target_x = 0
#         target_y += tile_h

# minecart
target_x = 0
target_y = tile_h * 7
tile_id = tileset_cols * 8

tile_filenames = sorted(glob.glob(output_path + "minecart/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_short_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# objects
target_x = 0
target_y = tile_h * 8
tile_id = tileset_cols * 9

tile_filenames = sorted(glob.glob(output_path + "objects/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i == 10:
        # containers are on the next 2 rows
        target_x = 0
        target_y += tile_h
        tile_id += 6
    elif i == 14:
        # corner walls are back on the previous row, target_x lines up still
        target_x = 0
        target_y += tile_h
        tile_id += 12

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# water
target_x = 0
target_y = tile_h * 11
tile_id = tileset_cols * 12

tile_filenames = sorted(glob.glob(output_path + "water/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i < 28:
        tiled_tile = tile.crop((0, 0, tile.width, int(tile.height/2)))
        tile_sheet_tiled.alpha_composite(tiled_tile, (target_x, target_y + tile_floor_offset))

        if tile_id not in blank_tiles:
            tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_h * 0.625)))

        anim_defs[tile_id] = [(target_x, target_y, 250)]

    else:
        if i == 28:
            target_x = 0
            target_y = tile_h * 15
            tile_id = tileset_cols * 12

        if tile_id in anim_defs:
            anim_defs[tile_id].append((target_x, target_y, 250))

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# wooden walkways
target_x = 0
target_y = tile_h * 13
tile_id = tileset_cols * 14

tile_filenames = sorted(glob.glob(output_path + "wood_walk/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))

    tiled_tile = tile.crop((0, 0, tile.width, int(tile_floor_h * 1.5)))
    tile_sheet_tiled.alpha_composite(tiled_tile, (target_x, target_y + tile_short_offset + int(tile_floor_h / 2)))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_offset))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# portals
target_x = 0
target_y = tile_h * 14
tile_id = tileset_cols * 15

tile_filenames = sorted(glob.glob(output_path + "portals/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    # for crop_x in [(0, int(tile_w * 0.75)), (int(tile_w * 0.25), tile_w)]:
    #     tile_id += 1
    #     target_x += tile_w
    #     tile_cropped = tile.crop((crop_x[0], 0, crop_x[1], tile_h))
    #
    #     tile_sheet.alpha_composite(tile_cropped, (target_x + crop_x[0], target_y))
    #     tile_sheet_tiled.alpha_composite(tile_cropped, (target_x + crop_x[0], target_y))
    #
    #     if tile_id not in blank_tiles:
    #         tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# 2x2 (teleporter circle)
target_x = 0
target_y = tile_h * 17
tile_id = 264
anim_id = 265
anim_defs[anim_id] = []

tile_filenames = sorted(glob.glob(output_path + "../../teleport/output/*.png"))

# create the background for 2x2 tiles
tile_floor = Image.open(output_path + "floor/0001.png")
tile_floor_2x2 = Image.new('RGBA', (tile_w * 2, tile_h))
tile_floor_2x2_offsets = [ (int(tile_w/2), 0), (0, int(tile_floor_h/2)), (tile_w, int(tile_floor_h/2)), (int(tile_w/2), tile_floor_h) ]
for tile_offset in tile_floor_2x2_offsets:
    tile_floor_2x2.alpha_composite(tile_floor, (tile_offset[0], tile_offset[1]))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    for tile_offset in tile_floor_2x2_offsets:
        tile_sheet.alpha_composite(tile_floor, (target_x + tile_offset[0], target_y + tile_offset[1]))
    tile_sheet.alpha_composite(tile, (target_x, target_y))

    if i < 2:
        for tile_offset in tile_floor_2x2_offsets:
            tile_sheet_tiled_2x2.alpha_composite(tile_floor, (target_x + tile_offset[0], tile_offset[1]))
        tile_sheet_tiled_2x2.alpha_composite(tile, (target_x, 0))

        if tile_id not in blank_tiles:
            tile_defs.append((tile_id, target_x, target_y, tile_w*2, tile_floor_h*2, int(tile_w/2), tile_floor_h))

    if i > 0:
        anim_defs[anim_id].append((target_x, target_y, 66))

    tile_id += 1
    target_x += (tile_w * 2)
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# boss chest
target_x = 0
target_y = tile_h * 18
tile_id = 266

tile_filenames = sorted(glob.glob(output_path + "../../common/output/boss_chest/*.png"))

for i in range(0, len(tile_filenames)):
    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

        tile = Image.open(tile_filenames[i])

        tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))
        # TODO separate tilesheet for boss chest
        # tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h



# save the tilesheet files
tile_sheet.save(tile_sheet_filename)
tile_sheet_tiled.save(tile_sheet_tiled_filename)
tile_sheet_tiled_2x2.save(tile_sheet_tiled_2x2_filename)

# tilesetdef
tile_count = tileset_cols * tileset_rows
target_x = 0
target_y = 0

tile_defs.sort(key=lambda x:x[0])

tileset_def_filename = mod_path + 'tilesetdefs/tileset_cave.txt'
print('Writing tileset defintion file: ' + tileset_def_filename)
f = open(tileset_def_filename, 'w')
f.write('img=' + mod_image_path + 'tileset_cave.png\n\n')
for tile in tile_defs:
    f.write('tile=' + str(tile[0]) + ',')
    f.write(str(tile[1]) + ',' + str(tile[2]) + ',')
    f.write(str(tile[3]) + ',' + str(tile[4]) + ',')
    f.write(str(tile[5]) + ',' + str(tile[6]) + '\n')
for key, val in anim_defs.items():
    f.write('animation=' + str(key) + ';')
    for frame in val:
        f.write(str(frame[0]) + ',' + str(frame[1]) + ',' + str(frame[2]) + 'ms;')
    f.write('\n')

f.close()

flare_mod_path = "../../../mods/hd-flare-game/"
print("Copying to: " + flare_mod_path)
shutil.copytree(mod_path + mod_image_path, flare_mod_path + mod_image_path, dirs_exist_ok=True)
shutil.copytree(mod_path + mod_tilesetdef_path, flare_mod_path + mod_tilesetdef_path, dirs_exist_ok=True)
