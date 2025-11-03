#!/bin/sh

blender -b loot.blend --python-text Render
blender -b loot_coins.blend --python-text Render

