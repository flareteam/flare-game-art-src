#!/usr/bin/env python

import os

os.system('blender -b broken_tower.blend --python-text Render')
os.system('blender -b cabin.blend --python-text Render')
os.system('blender -b exit_markers.blend --python-text Render')
os.system('blender -b grassland_boat.blend --python-text Render')
os.system('blender -b grassland_bridge.blend --python-text Render')
os.system('blender -b grassland_containers.blend --python-text Render')
os.system('blender -b grassland_exits.blend --python-text Render')
os.system('blender -b grassland_fence.blend --python-text Render')
os.system('blender -b grassland_floor.blend --python-text Render')
os.system('blender -b grassland_objects.blend --python-text Render')
os.system('blender -b grassland_path.blend --python-text Render')
os.system('blender -b grassland_plants.blend --python-text Render')
os.system('blender -b grassland_props.blend --python-text Render')
os.system('blender -b grassland_rocks.blend --python-text Render')
os.system('blender -b grassland_shapes.blend --python-text Render')
os.system('blender -b grassland_tent.blend --python-text Render')
os.system('blender -b grassland_walls.blend --python-text Render')
os.system('blender -b grassland_water.blend --python-text Render')
os.system('blender -b rotten_tower.blend --python-text Render')
os.system('blender -b temple_entrance.blend --python-text Render')

os.system('blender -b tree_dead/dead_trees.blend --python-text Render')
os.system('blender -b tree_gum/gum_tree1.blend --python-text Render')
os.system('blender -b tree_two/two_trees.blend --python-text Render')
os.system('blender -b trunk/trunk.blend --python-text Render')

# TODO this only needs to be rendered once
#os.system('blender -b ../teleport/teleporter.blend --python-text Render')

