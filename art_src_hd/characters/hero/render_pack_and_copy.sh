#!/bin/sh

./render.sh

cd ../../mod_data/
./pack_animations.sh
./copy_to_mods.sh

