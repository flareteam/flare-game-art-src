#!/bin/sh

blender -b hobgoblin.blend --python-text RenderAll
blender -b hobgoblin_archer.blend --python-text RenderAll

