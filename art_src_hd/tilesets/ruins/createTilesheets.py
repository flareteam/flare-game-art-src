#!/usr/bin/env python

import os, sys, glob
import shutil
from PIL import Image

#os.system('blender -b old_ruins_tileset_source.blend --python-text RenderAll')

tile_w = 192
tile_h = 384
tile_floor_h = int(tile_h/4)
# tile_w = 64
# tile_h = 128
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

tileset_cols = 16
tileset_rows = 20
tileset_tiled_rows = tileset_rows - 4 # 2 animation rows + 2 rows for large stairs

tile_id_offset = 24

tile_defs = []
anim_defs = {}
blank_tiles = []
# blank_tiles = list(range(52, 56))
# blank_tiles += list(range(84, 88))
# blank_tiles += list(range(138, 144))
# blank_tiles += list(range(152, 160))
# blank_tiles += list(range(168, 176))
# blank_tiles += list(range(184, 192))

# create blank sheet images. The first one is a single sheet with everything on it for Flare. The others are split for usage in Tiled.
tile_sheet_filename = mod_path + mod_image_path + "tileset_ruins.png"
print("Writing tile sheet file: " + tile_sheet_filename)
tile_sheet = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_rows))

tile_sheet_tiled_filename = tiled_path + "ruins.png"
print("Writing tile sheet file: " + tile_sheet_tiled_filename)
tile_sheet_tiled = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_tiled_rows))

# tile_sheet_tiled_2x2_filename = tiled_path + "ruins_2x2.png"
# print("Writing tile sheet file: " + tile_sheet_tiled_2x2_filename)
# tile_sheet_tiled_2x2 = Image.new('RGBA', ((tile_w * 2) * 4, tile_h * 2))
#
# tile_sheet_tiled_doorleft_filename = tiled_path + "ruins_door_left.png"
# print("Writing tile sheet file: " + tile_sheet_tiled_doorleft_filename)
# tile_sheet_tiled_doorleft = Image.new('RGBA', (tile_w * 2, tile_h))
#
# tile_sheet_tiled_doorright_filename = tiled_path + "ruins_door_right.png"
# print("Writing tile sheet file: " + tile_sheet_tiled_doorright_filename)
# tile_sheet_tiled_doorright = Image.new('RGBA', (tile_w * 2, tile_h))
#
# tile_sheet_tiled_stairs_filename = tiled_path + "ruins_stairs.png"
# print("Writing tile sheet file: " + tile_sheet_tiled_stairs_filename)
# tile_sheet_tiled_stairs = Image.new('RGBA', (tile_w * 16, tile_h * 2))

tile_filenames = sorted(glob.glob(output_path + "floors/*.png"))
target_x = 0
target_y = 0

# first tile id is offset by one row (for collision tiles)
tile_id = tile_id_offset

# floors
for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# walls
target_x = 0
target_y = tile_h * 5
tile_id = tile_id_offset + (tileset_cols * 5)

tile_filenames = sorted(glob.glob(output_path + "walls/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# walls and objects
target_x = 0
target_y = tile_h * 9
tile_id = tile_id_offset + (tileset_cols * 9)

tile_filenames = sorted(glob.glob(output_path + "walls_and_objects/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# # 2x2 (teleporter circle)
# target_x = 0
# target_y = tile_h * 16
# tile_id = 264
# anim_id = 265
# anim_defs[anim_id] = []
#
# tile_filenames = sorted(glob.glob(output_path + "../../teleport/output/*.png"))
#
# # create the background for 2x2 tiles
# tile_floor = Image.open(output_path + "floors/0001.png")
# tile_floor_2x2 = Image.new('RGBA', (tile_w * 2, tile_h * 2))
# tile_floor_2x2_offsets = [ (int(tile_w/2), 0), (0, int(tile_floor_h/2)), (tile_w, int(tile_floor_h/2)), (int(tile_w/2), tile_floor_h) ]
# for tile_offset in tile_floor_2x2_offsets:
#     tile_floor_2x2.alpha_composite(tile_floor, (tile_offset[0], tile_offset[1]))
#
# for i in range(0, len(tile_filenames)):
#     tile = Image.open(tile_filenames[i])
#
#     for tile_offset in tile_floor_2x2_offsets:
#         tile_sheet.alpha_composite(tile_floor, (target_x + tile_offset[0], target_y + tile_offset[1]))
#     tile_sheet.alpha_composite(tile, (target_x, target_y))
#
#     if i < 2:
#         for tile_offset in tile_floor_2x2_offsets:
#             tile_sheet_tiled_2x2.alpha_composite(tile_floor, (target_x + tile_offset[0], tile_offset[1]))
#         tile_sheet_tiled_2x2.alpha_composite(tile, (target_x, 0))
#
#         if tile_id not in blank_tiles:
#             tile_defs.append((tile_id, target_x, target_y, tile_w*2, tile_floor_h*2, int(tile_w/2), tile_floor_h))
#
#     if i > 0:
#         anim_defs[anim_id].append((target_x, target_y, 66))
#
#     tile_id += 1
#     target_x += (tile_w * 2)
#     if target_x >= (tile_w * tileset_cols):
#         target_x = 0
#         target_y += tile_h


# boss chest
# target_x = 0
# target_y = tile_h * 19
# tile_id = 288
#
# tile_filenames = sorted(glob.glob(output_path + "../../common/output/boss_chest/*.png"))
#
# for i in range(0, len(tile_filenames)):
#     if tile_id not in blank_tiles:
#         tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))
#
#         tile = Image.open(tile_filenames[i])
#
#         tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))
#         # TODO separate tilesheet for boss chest
#         # tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))
#
#     tile_id += 1
#     target_x += tile_w
#     if target_x >= (tile_w * tileset_cols):
#         target_x = 0
#         target_y += tile_h


# save the tilesheet files
tile_sheet.save(tile_sheet_filename)
tile_sheet_tiled.save(tile_sheet_tiled_filename)
# tile_sheet_tiled_2x2.save(tile_sheet_tiled_2x2_filename)
# tile_sheet_tiled_doorleft.save(tile_sheet_tiled_doorleft_filename)
# tile_sheet_tiled_doorright.save(tile_sheet_tiled_doorright_filename)
# tile_sheet_tiled_stairs.save(tile_sheet_tiled_stairs_filename)

# tilesetdef
tile_count = tileset_cols * tileset_rows
target_x = 0
target_y = 0

tile_defs.sort(key=lambda x:x[0])

tileset_def_filename = mod_path + 'tilesetdefs/tileset_ruins.txt'
print('Writing tileset defintion file: ' + tileset_def_filename)
f = open(tileset_def_filename, 'w')
f.write('img=' + mod_image_path + 'tileset_ruins.png\n\n')
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
