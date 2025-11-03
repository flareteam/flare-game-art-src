#!/usr/bin/env python

import os, sys, glob
import shutil
from PIL import Image

#os.system('blender -b floors.blend --python-text RenderAll')
#os.system('blender -b classicdungeon.blend --python-text RenderAll')
#os.system('blender -b low_walls.blend --python-text RenderAll')
#os.system('blender -b runes.blend --python-text RenderAll')

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
tileset_tiled_rows = tileset_rows - 5 # 2 animation rows + 2 rows for large stairs + 1 for boss chest

tile_defs = []
anim_defs = {}
blank_tiles = list(range(53, 56))
blank_tiles += list(range(84, 88))
blank_tiles += list(range(138, 144))
blank_tiles += list(range(152, 160))
blank_tiles += list(range(168, 176))
blank_tiles += list(range(184, 192))

# create blank sheet images. The first one is a single sheet with everything on it for Flare. The others are split for usage in Tiled.
tile_sheet_filename = mod_path + mod_image_path + "tileset_dungeon.png"
print("Writing tile sheet file: " + tile_sheet_filename)
tile_sheet = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_rows))

tile_sheet_tiled_filename = tiled_path + "dungeon.png"
print("Writing tile sheet file: " + tile_sheet_tiled_filename)
tile_sheet_tiled = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_tiled_rows))

tile_sheet_tiled_2x2_filename = tiled_path + "dungeon_2x2.png"
print("Writing tile sheet file: " + tile_sheet_tiled_2x2_filename)
tile_sheet_tiled_2x2 = Image.new('RGBA', ((tile_w * 2) * 4, tile_h * 2))

tile_sheet_tiled_doorleft_filename = tiled_path + "dungeon_door_left.png"
print("Writing tile sheet file: " + tile_sheet_tiled_doorleft_filename)
tile_sheet_tiled_doorleft = Image.new('RGBA', (tile_w * 2, tile_h))

tile_sheet_tiled_doorright_filename = tiled_path + "dungeon_door_right.png"
print("Writing tile sheet file: " + tile_sheet_tiled_doorright_filename)
tile_sheet_tiled_doorright = Image.new('RGBA', (tile_w * 2, tile_h))

tile_sheet_tiled_stairs_filename = tiled_path + "dungeon_stairs.png"
print("Writing tile sheet file: " + tile_sheet_tiled_stairs_filename)
tile_sheet_tiled_stairs = Image.new('RGBA', (tile_w * 16, tile_h * 2))

tile_filenames = sorted(glob.glob(output_path + "floors/*.png"))
target_x = 0
target_y = 0

# first tile id is offset by one row (for collision tiles)
tile_id = tileset_cols

# floors
for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    # floor tiles are out of order
    if i == 4:
        # cracked floor tiles
        target_y += tile_h
        tile_id = (tileset_cols * 2) + 4
    elif i == 16:
        # small floor tiles
        target_x = 0
        target_y = tile_h
        tile_id = tileset_cols * 2
    elif i == 20:
        # raised border floor tiles
        target_x = tile_w * 4
        target_y = 0
        tile_id = tileset_cols + 4

    # composite the raised border tiles with a plain floor tile
    if i >= 20:
        tile_base = Image.open(tile_filenames[0])
        tile_sheet.alpha_composite(tile_base, (target_x, target_y + tile_floor_offset))
        tile_sheet_tiled.alpha_composite(tile_base, (target_x, target_y + tile_floor_offset))

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# pits
target_x = 0
target_y = tile_h * 2
tile_id = tileset_cols * 3

tile_filenames = sorted(glob.glob(output_path + "low_walls/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_flare = Image.new('RGBA', (tile_w, tile_h))
    tile_tiled = Image.new('RGBA', (tile_w, tile_h))

    # flare tileset
    if i == 1:
        tile_temp = tile.crop((0, 0, int(tile_w/2), tile_h))
        tile_flare.alpha_composite(tile_temp, (0, 0))
    elif i == 2:
        tile_temp = tile.crop((int(tile_w/2), 0, tile_w, tile_h))
        tile_flare.alpha_composite(tile_temp, (int(tile_w/2), 0))
    else:
        tile_flare = tile

    # tiled tileset
    tile_temp = tile_flare.crop((0, 0, tile_w, tile_h - tile_floor_offset))
    tile_tiled.alpha_composite(tile_temp, (0, tile_floor_offset))

    tile_sheet.alpha_composite(tile_flare, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile_tiled, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_h - int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# floor grate
target_x = tile_w * 3
target_y = tile_h * 2
tile_id = (tileset_cols * 3) + 3

tile_filenames = sorted(glob.glob(output_path + "floor_grate/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# rune floor tiles
target_x = tile_w * 8
target_y = tile_h * 2
tile_id = (tileset_cols * 3) + 8

tile_filenames = sorted(glob.glob(output_path + "runes/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

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

# barricades
target_x = tile_w * 6
target_y = tile_h * 6
tile_id = (tileset_cols * 7) + 6

tile_filenames = sorted(glob.glob(output_path + "barricade/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_short_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# objects
target_x = 0
target_y = tile_h * 7
tile_id = tileset_cols * 8

tile_filenames = sorted(glob.glob(output_path + "objects/*.png"))

for i in range(0, len(tile_filenames)):
    # stop at the lit brazier. We'll use a frame from the actual animation for this
    if i == 27:
        break

    # skip blank animation frames
    if i == 18 or i == 19:
        continue

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

        tile = Image.open(tile_filenames[i])

        tile_sheet.alpha_composite(tile, (target_x, target_y))
        tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if i == 9:
        # wrap to second row
        tile_id += 7
        target_x = 0
        target_y += tile_h
    elif i == 17:
        # wrap to third row
        tile_id += 9
        target_x = 0
        target_y += tile_h
    else:
        tile_id += 1
        target_x += tile_w

    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# lit brazier
target_x = tile_w * 7
target_y = tile_h * 9
tile_id = (tileset_cols * 10) + 7

tile_filenames = sorted(glob.glob(output_path + "brazier/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i == 0:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))
        tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))
        target_x = 0
        target_y = tile_h * 15
        anim_defs[tile_id] = []


    tile_sheet.alpha_composite(tile, (target_x, target_y))
    anim_defs[tile_id].append((target_x, target_y, 66))

    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# bones
target_x = 0
target_y = tile_h * 10
tile_id = tileset_cols * 11

tile_filenames = sorted(glob.glob(output_path + "bones/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_floor_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# long chains
target_x = 0
target_y = tile_h * 11
tile_id = tileset_cols * 12

tile_filenames = sorted(glob.glob(output_path + "chains/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i == 0:
        tile_cropped = tile.crop((int(tile_w*0.5), 0, int(tile_w*1.5), tile_h))
        tile_sheet_tiled.alpha_composite(tile_cropped, (target_x, target_y))
        tile_sheet.alpha_composite(tile, (target_x, target_y))
    elif i == 1:
        target_x = tile_w
        tile_cropped = tile.crop((int(tile_w*0.5), 0, int(tile_w*1.5), tile_h))
        tile_sheet_tiled.alpha_composite(tile_cropped, (target_x, target_y))
        target_x = tile_w * 2
        tile_sheet.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w*2, tile_h, tile_w, int(tile_floor_center_h)))

    tile_id += 1


# tomb and bed
target_x = tile_w * 4
target_y = tile_h * 11
tile_id = (tileset_cols * 12) + 2

tall_slices = 3
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "tomb/*.png"))
tile_filenames += sorted(glob.glob(output_path + "bed/*.png"))

for i in range(0, len(tile_filenames)):

    if i == 0 or i == 3 or i == 5:
        # facing north/south
        corner_slice = 0
    elif i == 1 or i == 2 or i == 4:
        # facing west/east
        corner_slice = 1
    else:
        continue

    tile = Image.open(tile_filenames[i])
    top_pad = tile_h - tile.size[1]

    for j in range(0, tall_slices):
        # left or right
        slice_col = j % 2

        if j == corner_slice:
            slice_offset_x = 0
            slice_offset_y = 0
        elif j > corner_slice:
            slice_offset_x = tall_slice_w
            slice_offset_y = abs(j - corner_slice - 1) * tile_large_offset_step
        else:
            slice_offset_x = 0
            slice_offset_y = abs(j - corner_slice) * tile_large_offset_step

        tile_cropped = tile.crop((j * tall_slice_w, 0, (j * tall_slice_w) + tall_slice_w, tile_h - slice_offset_y))

        tile_sheet.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))
        # tile_sheet_tiled.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h


# doors
# We start with the closed doors, which aren't on the Tiled sheet, but ARE on the Flare sheet.
# The Flare sheet has an empty row below the open doors, so we'll put them there. This will need to change if we decide to use that row for new tiles.
target_x = 0
target_y = tile_h * 13
tile_id = 280

tile_filenames = sorted(glob.glob(output_path + "doors/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    # for closed doors
    door_offset_x = 0
    door_offset_y = 0

    if i < 2:
        # door closed left
        tile_sheet.alpha_composite(tile, (target_x, target_y))
        tile_sheet_tiled_doorleft.alpha_composite(tile, (target_x, 0))
        door_offset_x = -48
        door_offset_y = -24
    elif i < 4:
        # door closed right
        tile_sheet.alpha_composite(tile, (target_x, target_y))
        tile_sheet_tiled_doorright.alpha_composite(tile, (target_x - (tile_w * 2), 0))
        door_offset_x = 48
        door_offset_y = -24
    else:
        # open doors
        # we're done with the closed doors, reset our target/id for placing the open doors on both tilesheets
        if i == 4:
            target_x = 0
            target_y = tile_h * 12
            tile_id = tileset_cols * 13

        tile_sheet.alpha_composite(tile, (target_x, target_y))
        tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2) - door_offset_x, int(tile_floor_center_h) - door_offset_y))

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

    for crop_x in [(0, int(tile_w * 0.75)), (int(tile_w * 0.25), tile_w)]:
        tile_id += 1
        target_x += tile_w
        tile_cropped = tile.crop((crop_x[0], 0, crop_x[1], tile_h))

        tile_sheet.alpha_composite(tile_cropped, (target_x + crop_x[0], target_y))
        tile_sheet_tiled.alpha_composite(tile_cropped, (target_x + crop_x[0], target_y))

        if tile_id not in blank_tiles:
            tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), int(tile_floor_center_h)))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# 2x2 (teleporter circle)
target_x = 0
target_y = tile_h * 16
tile_id = 264
anim_id = 265
anim_defs[anim_id] = []

tile_filenames = sorted(glob.glob(output_path + "../../teleport/output/*.png"))

# create the background for 2x2 tiles
tile_floor = Image.open(output_path + "floors/0001.png")
tile_floor_2x2 = Image.new('RGBA', (tile_w * 2, tile_h * 2))
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


# 4x4 (large stairs)
target_x = 0
target_y = tile_h * 17
tile_id = 284

tile_filenames = sorted(glob.glob(output_path + "stairs/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled_stairs.alpha_composite(tile, (target_x, 0))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w*4, tile_h*2, int(tile_w/2), int(tile_h * 1.5)))

    tile_id += 1
    target_x += (tile_w * 4)
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += (tile_h * 2)


# boss chest
target_x = 0
target_y = tile_h * 19
tile_id = 288

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
tile_sheet_tiled_doorleft.save(tile_sheet_tiled_doorleft_filename)
tile_sheet_tiled_doorright.save(tile_sheet_tiled_doorright_filename)
tile_sheet_tiled_stairs.save(tile_sheet_tiled_stairs_filename)

# tilesetdef
tile_count = tileset_cols * tileset_rows
target_x = 0
target_y = 0

tile_defs.sort(key=lambda x:x[0])

tileset_def_filename = mod_path + 'tilesetdefs/tileset_dungeon.txt'
print('Writing tileset defintion file: ' + tileset_def_filename)
f = open(tileset_def_filename, 'w')
f.write('img=' + mod_image_path + 'tileset_dungeon.png\n\n')
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
