#!/usr/bin/env python

import os

os.system('blender -b cave_floors.blend --python-text Render')

# TODO this only needs to be rendered once
#os.system('blender -b ../teleport/teleporter.blend --python-text Render')

