#!/usr/bin/env python

import os

os.system('blender -b floors.blend --python-text Render')
os.system('blender -b low_walls.blend --python-text Render')
os.system('blender -b floor_grate.blend --python-text Render')
os.system('blender -b runes.blend --python-text Render')

os.system('blender -b classicdungeon.blend --python-text Render')
os.system('blender -b barricade_tiles.blend --python-text Render')
os.system('blender -b classicobjects.blend --python-text Render')
os.system('blender -b brazier.blend --python-text Render')
os.system('blender -b bone_rubble.blend --python-text Render')
os.system('blender -b long_chains.blend --python-text Render')
os.system('blender -b tombwoof.blend --python-text Render')
os.system('blender -b bed.blend --python-text Render')

# TODO this only needs to be rendered once
os.system('blender -b ../teleport/teleporter.blend --python-text Render')

