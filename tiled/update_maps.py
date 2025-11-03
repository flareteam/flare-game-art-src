#!/usr/bin/env python

import glob
import xml.etree.ElementTree as ET

replaced_image_dir = '../../../mods/hd-flare-game/tiled/tilesheets/'

replaced_images = []

# common
replaced_images.append(('boss_chest.png', replaced_image_dir + 'boss_chest.png'))
replaced_images.append(('set_rules.png', replaced_image_dir + 'tiled_set_rules.png'))
replaced_images.append(('tiled_collision.png', replaced_image_dir + 'tiled_collision.png'))

# cave
replaced_images.append(('tiled_cave.png', replaced_image_dir + 'cave.png'))
replaced_images.append(('tiled_cave_2x2.png', replaced_image_dir + 'cave_2x2.png'))

# dungeon
replaced_images.append(('tiled_dungeon.png', replaced_image_dir + 'dungeon.png'))
replaced_images.append(('tiled_dungeon_2x2.png', replaced_image_dir + 'dungeon_2x2.png'))
replaced_images.append(('door_left.png', replaced_image_dir + 'dungeon_door_left.png'))
replaced_images.append(('door_right.png', replaced_image_dir + 'dungeon_door_right.png'))
replaced_images.append(('stairs.png', replaced_image_dir + 'dungeon_stairs.png'))

# snowplains
replaced_images.append(('snowplains.png', replaced_image_dir + 'snowplains.png'))
replaced_images.append(('snowplains_water.png', replaced_image_dir + 'snowplains_water.png'))
replaced_images.append(('snowplains_structures.png', replaced_image_dir + 'snowplains_structures.png'))
replaced_images.append(('snowplains_trees.png', replaced_image_dir + 'snowplains_trees.png'))
replaced_images.append(('snowplains_ice.png', replaced_image_dir + 'snowplains_ice.png'))
replaced_images.append(('snowplains_other.png', replaced_image_dir + 'snowplains_other.png'))
replaced_images.append(('tiled_snowplains_2x2.png', replaced_image_dir + 'snowplains_2x2.png'))
replaced_images.append(('snowplains_rottentower.png', replaced_image_dir + 'snowplains_rottentower.png'))

# grassland
replaced_images.append(('grassland.png', replaced_image_dir + 'grassland.png'))
replaced_images.append(('grassland_water.png', replaced_image_dir + 'grassland_water.png'))
replaced_images.append(('grassland_structures.png', replaced_image_dir + 'grassland_structures.png'))
replaced_images.append(('grassland_trees.png', replaced_image_dir + 'grassland_trees.png'))
replaced_images.append(('tiled_grassland_2x2.png', replaced_image_dir + 'grassland_2x2.png'))
# MAKE SURE THIS ONE IS CHECKED AFTER THE SNOWPLAINS VARIANT
replaced_images.append(('rottentower.png', replaced_image_dir + 'grassland_rottentower.png'))


target_tile_w = 192
target_tile_h = 96
target_scale = 3


def processTMX(filename):
    print("Processing: " + filename)

    tree = ET.parse(filename)
    root = tree.getroot() # <map>

    tile_w = root.get('tilewidth')
    tile_h = root.get('tileheight')

    updated = int(tile_w) == target_tile_w and int(tile_h) == target_tile_h

    for tileset in root.findall('tileset'):
        if not updated:
            tileset.set('tilewidth', str(int(tileset.get('tilewidth')) * target_scale))
            tileset.set('tileheight', str(int(tileset.get('tileheight')) * target_scale))

            tile_offset = tileset.find('tileoffset')
            if tile_offset != None:
                tile_offset.set('x', str(int(tile_offset.get('x')) * target_scale))
                tile_offset.set('y', str(int(tile_offset.get('y')) * target_scale))

        tileset_image = tileset.find('image')
        if tileset_image != None:
            if not updated:
                tileset_image.set('width', str(int(tileset_image.get('width')) * target_scale))
                tileset_image.set('height', str(int(tileset_image.get('height')) * target_scale))

            image_source = tileset_image.get('source')
            for replacement in replaced_images:
                if image_source.endswith(replacement[0]):
                    image_source_replaced = image_source.replace(replacement[0], replacement[1])
                    tileset_image.set('source', image_source_replaced)
                    break

    if not updated:
        root.set('tilewidth', str(target_tile_w))
        root.set('tileheight', str(target_tile_h))

        for objgroup in root.findall('objectgroup'):
            for obj in objgroup.findall('object'):
                x = obj.get('x')
                y = obj.get('y')
                width = obj.get('width')
                height = obj.get('height')
                if x != None:
                    obj.set('x', str(int(x) * target_scale))
                if y != None:
                    obj.set('y', str(int(y) * target_scale))
                if width != None:
                    obj.set('width', str(int(width) * target_scale))
                if height != None:
                    obj.set('height', str(int(height) * target_scale))

        tree.write(filename)

map_filenames = sorted(glob.glob("../../../game/tiled/**/*.tmx", recursive=True))
for map_file in map_filenames:
    processTMX(map_file)
