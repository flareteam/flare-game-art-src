#!/usr/bin/env python

import os, sys, glob
import shutil
from PIL import Image

tile_w = 192
tile_h = 384
tile_tall_h = tile_h * 2
tile_floor_h = int(tile_h/4)
tile_floor_offset = int(tile_h * 0.75)
tile_short_offset = int(tile_h * 0.5)
tile_floor_center_h = int(tile_h * 0.875)
tile_large_offset_step = int(tile_h * 0.125)
tile_small_object_offset = int(tile_h * 0.375)
tile_water_offset = int(tile_h * 0.625)

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
tileset_rows = 18
tileset_tiled_rows = 8
tileset_tiled_water_rows = 4
tileset_tiled_structures_rows = 4
tileset_tiled_trees_rows = 4

tile_defs = []
tile_defs_water = []
anim_defs = {}
anim_defs_water = {}
blank_tiles = []

water_anim_frame_time = 250

# create blank sheet images. The first one is a single sheet with everything on it for Flare. The others are split for usage in Tiled.
tile_sheet_filename = mod_path + mod_image_path + "tileset_grassland.png"
print("Writing tile sheet file: " + tile_sheet_filename)
tile_sheet = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_rows))

tile_sheet_water_filename = mod_path + mod_image_path + "tileset_grassland_water.png"
print("Writing tile sheet file: " + tile_sheet_water_filename)
tile_sheet_water = Image.new('RGBA', (tile_w * tileset_cols, tile_h * 8))

tile_sheet_tiled_filename = tiled_path + "grassland.png"
print("Writing tile sheet file: " + tile_sheet_tiled_filename)
tile_sheet_tiled = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_tiled_rows))

tile_sheet_tiled_water_filename = tiled_path + "grassland_water.png"
print("Writing tile sheet file: " + tile_sheet_tiled_water_filename)
tile_sheet_tiled_water = Image.new('RGBA', (tile_w * tileset_cols, int(tile_h /2) * tileset_tiled_water_rows))

tile_sheet_tiled_structures_filename = tiled_path + "grassland_structures.png"
print("Writing tile sheet file: " + tile_sheet_tiled_structures_filename)
tile_sheet_tiled_structures = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_tiled_structures_rows))

tile_sheet_tiled_trees_filename = tiled_path + "grassland_trees.png"
print("Writing tile sheet file: " + tile_sheet_tiled_trees_filename)
tile_sheet_tiled_trees = Image.new('RGBA', (tile_w * tileset_cols, tile_h * tileset_tiled_trees_rows))

tile_sheet_tiled_2x2_filename = tiled_path + "grassland_2x2.png"
print("Writing tile sheet file: " + tile_sheet_tiled_2x2_filename)
tile_sheet_tiled_2x2 = Image.new('RGBA', ((tile_w * 2) * 4, tile_h * 4))

tile_sheet_tiled_rottentower_filename = tiled_path + "grassland_rottentower.png"
print("Writing tile sheet file: " + tile_sheet_tiled_rottentower_filename)
rottentower_src = Image.open(output_path + "rotten_tower/0001.png")
tile_sheet_tiled_rottentower = Image.new('RGBA', (rottentower_src.width, rottentower_src.height))

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

# stone path
tile_filenames = sorted(glob.glob(output_path + "floor_path/*.png"))
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

# walls
target_x = 0
target_y = tile_h * 2
tile_id = tileset_cols * 3

tile_filenames = sorted(glob.glob(output_path + "walls/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i == 24:
        break

    tile_sheet.alpha_composite(tile, (target_x, target_y))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# containers
target_x = 0
target_y = tile_h * 5
tile_id = tileset_cols * 6

tile_filenames = sorted(glob.glob(output_path + "containers/*.png"))

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

# objects (camp)
target_x = tile_w * 4
target_y = tile_h * 5
tile_id = (tileset_cols * 6) + 4

tile_filenames = sorted(glob.glob(output_path + "objects/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    # empty stump and stump with axe are placed further down
    if i == 4:
        target_x = tile_w * 8
        target_y = tile_h * 7
        tile_id = (tileset_cols * 8) + 8

    tile_sheet.alpha_composite(tile, (target_x, target_y + tile_short_offset))
    tile_sheet_tiled.alpha_composite(tile, (target_x, target_y + tile_short_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# tent
target_x = tile_w * 8
target_y = tile_h * 3
tile_id = (tileset_cols * 4) + 8

tall_slices = 3
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "tent/*.png"))

for i in range(0, len(tile_filenames)):

    if i == 0:
        # facing north/south
        corner_slice = 0
    elif i == 1:
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
        tile_sheet_tiled.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h

# trunk
target_x = tile_w * 12
target_y = tile_h * 3
tile_id = (tileset_cols * 4) + 12

tile_filenames = sorted(glob.glob(output_path + "trunk/*.png"))

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

# exit markers
target_x = tile_w * 12
target_y = tile_h * 4
tile_id = (tileset_cols * 5) + 12

tile_filenames = sorted(glob.glob(output_path + "exit_markers/*.png"))

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

# fence
target_x = tile_w * 8
target_y = tile_h * 5
tile_id = (tileset_cols * 6) + 8

tall_slices = 3
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "fence/*.png"))

for i in range(0, len(tile_filenames)):

    # note: this is slightly different than the other "tall" tiles, in that the output render isn't centered on the tile.
    # slice_offset is used to account for that
    if i == 0 or i == 2:
        # facing north/south
        corner_slice = 0
        slice_offset = tall_slice_w
    elif i == 1 or i == 3:
        # facing west/east
        corner_slice = 1
        slice_offset = 0
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

        tile_cropped = tile.crop(((j * tall_slice_w) + slice_offset, 0, (j * tall_slice_w) + tall_slice_w + slice_offset, tile_h - slice_offset_y))

        tile_sheet.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))
        tile_sheet_tiled.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h

# plants
target_x = 0
target_y = tile_h * 6
tile_id = tileset_cols * 7

tile_filenames = sorted(glob.glob(output_path + "plants/*.png"))

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

# rocks
target_x = 0
target_y = tile_h * 7
tile_id = tileset_cols * 8

tile_filenames = sorted(glob.glob(output_path + "rocks/*.png"))

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

# props
target_x = tile_w * 10
target_y = tile_h * 7
tile_id = (tileset_cols * 8) + 10

tile_filenames = sorted(glob.glob(output_path + "props/*.png"))

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



# water walls
target_x = 0
target_y = 0
tile_id = tileset_cols * 9

tile_filenames = sorted(glob.glob(output_path + "walls/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i < 24:
        continue

    if i < 48:
        tiled_tile = tile.crop((0, int(tile_h / 2), tile_w, tile_h))
        tiled_target_y = int(target_y / 2)
        tile_sheet_tiled_water.alpha_composite(tiled_tile, (target_x, tiled_target_y))

        if tile_id not in blank_tiles:
            tile_defs_water.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_water_offset))

        anim_defs_water[tile_id] = [(target_x, target_y, water_anim_frame_time)]
    else:
        if i == 48:
            target_x = 0
            target_y = tile_h * 4
            tile_id = tileset_cols * 9

        if tile_id in anim_defs_water:
            anim_defs_water[tile_id].append((target_x, target_y, water_anim_frame_time))

    tile_sheet_water.alpha_composite(tile, (target_x, target_y))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# boat
target_x = tile_w * 8
target_y = tile_h
tile_id = (tileset_cols * 10) + 8
tiled_y_offset = 0

tall_slices = 4
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "boat/*.png"))

for i in range(0, len(tile_filenames)):

    if i == 0:
        # facing west/east
        corner_slice = 2
    elif i == 1:
        # facing north/south
        corner_slice = 0
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

        tile_sheet_water.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))

        tile_sheet_tiled_water.alpha_composite(tile_cropped, (target_x + slice_offset_x, tiled_y_offset + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs_water.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_water_offset))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h

# water
target_x = 0
target_y = tile_h * 2
tile_id = tileset_cols * 11

tile_filenames = sorted(glob.glob(output_path + "water/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i < 16:
        tiled_target_y = int(target_y / 2)
        tile_sheet_tiled_water.alpha_composite(tile, (target_x, tiled_target_y + tile_floor_h))

        if tile_id not in blank_tiles:
            tile_defs_water.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_water_offset))

        anim_defs_water[tile_id] = [(target_x, target_y, water_anim_frame_time)]
    else:
        if i == 16:
            target_x = 0
            target_y = tile_h * 6
            tile_id = tileset_cols * 11

        if tile_id in anim_defs_water:
            anim_defs_water[tile_id].append((target_x, target_y, water_anim_frame_time))

    tile_sheet_water.alpha_composite(tile, (target_x, target_y + tile_floor_offset))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# bridge
target_x = 0
target_y = tile_h * 3
tile_id = tileset_cols * 12

tile_filenames = sorted(glob.glob(output_path + "water_bridge/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    if i < 16:
        tiled_tile = tile.crop((0, int(tile_h / 2), tile_w, tile_h))
        tiled_target_y = int(target_y / 2)
        tile_sheet_tiled_water.alpha_composite(tiled_tile, (target_x, tiled_target_y))

        if tile_id not in blank_tiles:
            tile_defs_water.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_water_offset))

        anim_defs_water[tile_id] = [(target_x, target_y, water_anim_frame_time)]
    else:
        if i == 16:
            target_x = 0
            target_y = tile_h * 7
            tile_id = tileset_cols * 12

        if tile_id in anim_defs_water:
            anim_defs_water[tile_id].append((target_x, target_y, water_anim_frame_time))

    tile_sheet_water.alpha_composite(tile, (target_x, target_y))

    tile_id += 1
    target_x += tile_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# cabin
target_x = 0
target_y = tile_h * 8
tile_id = tileset_cols * 13
tiled_y_offset = tile_h * 8

tall_slices = 5
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "cabin/*.png"))

for i in range(0, len(tile_filenames)):

    if i == 0:
        # facing north/south
        corner_slice = 1
    elif i == 1:
        # facing west/east
        corner_slice = 2
    else:
        continue

    tile = Image.open(tile_filenames[i])
    top_pad = tile_tall_h - tile.size[1]

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

        tile_cropped = tile.crop((j * tall_slice_w, 0, (j * tall_slice_w) + tall_slice_w, tile_tall_h - slice_offset_y))

        tile_sheet.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))

        tile_sheet_tiled_structures.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y - tiled_y_offset + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_tall_h, int(tile_w/2), tile_h + tile_floor_center_h))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_tall_h

# temple entrance
target_x = tile_w * 8
target_y = tile_h * 8
tile_id = (tileset_cols * 13) + 8
tiled_y_offset = tile_h * 8

tall_slices = 8
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "broken_tower/*.png"))

for i in range(0, len(tile_filenames)):

    corner_slice = 3

    tile = Image.open(tile_filenames[i])
    top_pad = tile_tall_h - tile.size[1]

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

        tile_cropped = tile.crop((j * tall_slice_w, 0, (j * tall_slice_w) + tall_slice_w, tile_tall_h - slice_offset_y))

        tile_sheet.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y + slice_offset_y + top_pad))

        tile_sheet_tiled_structures.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y - tiled_y_offset + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_tall_h, int(tile_w/2), int(tile_tall_h - (tile_floor_h/2))))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h

# cave/mine exits
target_x = 0
target_y = tile_h * 10
tile_id = tileset_cols * 14
tiled_y_offset = tile_h * 7

tall_slices = 3
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "cave_exits/*.png"))

for i in range(0, len(tile_filenames)):

    if i == 0 or i == 2:
        # facing west
        corner_slice = 0
    elif i == 1 or i == 3:
        # facing north
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

        tile_sheet_tiled_structures.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y - tiled_y_offset + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h

# temple entrance
target_x = tile_w * 8
target_y = tile_h * 10
tile_id = (tileset_cols * 14) + 8
tiled_y_offset = tile_h * 7

tall_slices = 8
tall_slice_w = int(tile_w/2)

tile_filenames = sorted(glob.glob(output_path + "temple_entrance/*.png"))

for i in range(0, len(tile_filenames)):

    corner_slice = 3

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

        tile_sheet_tiled_structures.alpha_composite(tile_cropped, (target_x + slice_offset_x, target_y - tiled_y_offset + slice_offset_y + top_pad))

        if j < corner_slice or j >= corner_slice + 1:
            if tile_id not in blank_tiles:
                tile_defs.append((tile_id, target_x, target_y, tile_w, tile_h, int(tile_w/2), tile_floor_center_h))

            # whole tile complete, increment to next tile
            tile_id += 1
            target_x += tile_w
            if target_x >= (tile_w * tileset_cols):
                target_x = 0
                target_y += tile_h

# gum tree
target_x = 0
target_y = tile_h * 12
tile_id = tileset_cols * 15
tiled_y_offset = tile_h * 11

tile_filenames = sorted(glob.glob(output_path + "tree_gum/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))

    tile_sheet_tiled_trees.alpha_composite(tile, (target_x, target_y - tiled_y_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w*2, tile_h, tile_w, tile_floor_center_h))

    tile_id += 1
    target_x += tile_w * 2
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# dead trees
target_x = tile_w * 8
target_y = tile_h * 11
tile_id = (tileset_cols * 15) + 4
tiled_y_offset = tile_h * 11

tile_filenames = sorted(glob.glob(output_path + "tree_dead/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))

    tile_sheet_tiled_trees.alpha_composite(tile, (target_x, target_y - tiled_y_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w*2, tile_h*2, tile_w, tile_floor_center_h + tile_h))

    tile_id += 1
    target_x += tile_w * 2
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h


# deciduous and coniferous trees 
target_x = 0
target_y = tile_h * 13
tile_id = (tileset_cols * 15) + 8
tiled_y_offset = tile_h * 11

tile_filenames = sorted(glob.glob(output_path + "tree_two/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))

    tile_sheet_tiled_trees.alpha_composite(tile, (target_x, target_y - tiled_y_offset))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x, target_y, tile_w*2, tile_h*2, tile_w, tile_floor_center_h + tile_h))

    tile_id += 1
    target_x += tile_w * 2
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tile_h

# 2x2 (teleporter circle)
target_x = 0
target_y = tile_h * 15
tile_id = 264
anim_id = 265
anim_defs[anim_id] = []

tile_filenames = sorted(glob.glob(output_path + "../../teleport/output/*.png"))

# create the background for 2x2 tiles
tile_floor = Image.open(output_path + "floor/0001.png")
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


# rotten tower
target_x = tile_w * 10
target_y = tile_h * 15
tile_id = 296

tower_tex_size = 1074
tower_w = 960
tower_h = 1056
tower_offset_x = int((tower_tex_size - tower_w)/2)

tile_filenames = sorted(glob.glob(output_path + "rotten_tower/*.png"))

for i in range(0, len(tile_filenames)):
    tile = Image.open(tile_filenames[i])

    tile_sheet.alpha_composite(tile, (target_x, target_y))

    tile_sheet_tiled_rottentower.alpha_composite(tile, (0, 0))

    if tile_id not in blank_tiles:
        tile_defs.append((tile_id, target_x + tower_offset_x, target_y, tower_w, tower_h, int(tower_w * 0), int(tower_h * (300/352)) ))

    tile_id += 1
    target_x += tower_w
    if target_x >= (tile_w * tileset_cols):
        target_x = 0
        target_y += tower_h

# boss chest
target_x = 0
target_y = tile_h * 17
tile_id = 297

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
tile_sheet_water.save(tile_sheet_water_filename)

tile_sheet_tiled.save(tile_sheet_tiled_filename)
tile_sheet_tiled_water.save(tile_sheet_tiled_water_filename)
tile_sheet_tiled_structures.save(tile_sheet_tiled_structures_filename)
tile_sheet_tiled_trees.save(tile_sheet_tiled_trees_filename)
tile_sheet_tiled_2x2.save(tile_sheet_tiled_2x2_filename)
tile_sheet_tiled_rottentower.save(tile_sheet_tiled_rottentower_filename)

# tilesetdef
tile_count = tileset_cols * tileset_rows
target_x = 0
target_y = 0

tile_defs.sort(key=lambda x:x[0])

tileset_images = [
    ('tileset_grassland.png', tile_defs, anim_defs),
    ('tileset_grassland_water.png', tile_defs_water, anim_defs_water),
]

tileset_def_filename = mod_path + 'tilesetdefs/tileset_grassland.txt'
print('Writing tileset defintion file: ' + tileset_def_filename)
f = open(tileset_def_filename, 'w')
for img in tileset_images:
    f.write('[tileset]\n')
    f.write('img=' + mod_image_path + img[0] +'\n\n')
    for tile in img[1]:
        f.write('tile=' + str(tile[0]) + ',')
        f.write(str(tile[1]) + ',' + str(tile[2]) + ',')
        f.write(str(tile[3]) + ',' + str(tile[4]) + ',')
        f.write(str(tile[5]) + ',' + str(tile[6]) + '\n')
    for key, val in img[2].items():
        f.write('animation=' + str(key) + ';')
        for frame in val:
            f.write(str(frame[0]) + ',' + str(frame[1]) + ',' + str(frame[2]) + 'ms;')
        f.write('\n')

f.close()

flare_mod_path = "../../../mods/hd-flare-game/"
print("Copying to: " + flare_mod_path)
shutil.copytree(mod_path + mod_image_path, flare_mod_path + mod_image_path, dirs_exist_ok=True)
shutil.copytree(mod_path + mod_tilesetdef_path, flare_mod_path + mod_tilesetdef_path, dirs_exist_ok=True)
