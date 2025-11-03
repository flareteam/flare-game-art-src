#!/bin/sh

blender -b peasant_man1.blend --python-text RenderAll
blender -b peasant_man2.blend --python-text RenderAll
blender -b peasant_woman1.blend --python-text RenderAll
blender -b peasant_woman2.blend --python-text RenderAll

